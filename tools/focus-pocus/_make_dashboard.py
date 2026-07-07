import os, glob, json
from collections import defaultdict
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import gaussian_kde

# ---- palette (theme-light.scss) ----
NAVY  = "#1E3A6E"   # objective / measured
GOLD  = "#C29B2E"   # subjective / self-rating
PBLUE = "#7FA8D0"   # pastel blue (Panel D)
PGOLD = "#E0C98A"   # pastel gold (Panel D)
INK   = "#1C2433"
MUTED = "#8A8272"
GRID  = "#ECE7DA"
AXISC = "#C9C0AD"
GREY  = "#9AA0A6"
BG    = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": AXISC,
})

# ------------------------------------------------------------------ data source
HERE = os.path.dirname(os.path.abspath(__file__))

def _has_logs(p):
    return bool(p) and os.path.isdir(p) and any(f.endswith(".json") for f in os.listdir(p))

_FP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Focus-Pocus"))
SAMPLE_LOGS = os.path.join(_FP, "logs-sample")
_REAL = [os.environ.get("FP_LOGS"),
         os.path.join(os.path.expanduser("~"), "Documents", "FocusPocus", "logs"),
         os.path.join(_FP, "logs")]
LOGS = next((p for p in _REAL if _has_logs(p)), None)
USING_SAMPLE = False
if not LOGS:
    LOGS, USING_SAMPLE = SAMPLE_LOGS, True
    print("[!] No real logs found - falling back to SAMPLE dataset.")

ALERT_INTERVAL = 10 * 60 * 1000
MIN_FOCUS_MS   = 60_000
POMODORO_H     = 25 / 60
NORMAL_DAY_H   = 8.0

sessions = []
for fp in sorted(glob.glob(os.path.join(LOGS, "*.json"))):
    date = os.path.splitext(os.path.basename(fp))[0]
    with open(fp) as fh:
        for s in json.load(fh):
            if s.get("focusTime", 0) >= MIN_FOCUS_MS:
                s["_date"] = date
                sessions.append(s)

def measured_eff(s):
    prod = s["focusTime"] + s["procrastinationCount"] * ALERT_INTERVAL
    return round(100 * s["focusTime"] / prod) if prod > 0 else 0

sess_hours = np.array([s["focusTime"] / 3600000 for s in sessions])
rated      = [s for s in sessions if "efficiencyRating" in s]
self_sess  = np.array([s["efficiencyRating"] for s in rated], float)
meas_sess  = np.array([measured_eff(s) for s in rated], float)

day_hours, day_meas, day_self = defaultdict(float), defaultdict(list), defaultdict(list)
for s in sessions:
    day_hours[s["_date"]] += s["focusTime"] / 3600000
    day_meas[s["_date"]].append(measured_eff(s))
    if "efficiencyRating" in s:
        day_self[s["_date"]].append(s["efficiencyRating"])
days   = sorted(day_hours)
day_dt = [datetime.strptime(d, "%Y-%m-%d") for d in days]
hours  = np.array([day_hours[d] for d in days])

WK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
wk_hours = {i: [] for i in range(7)}
for d in days:
    wk_hours[datetime.strptime(d, "%Y-%m-%d").weekday()].append(day_hours[d])

# longest run of consecutive calendar days that were logged (Panel A)
best_s = best_e = s0 = 0
for i in range(1, len(day_dt)):
    if (day_dt[i] - day_dt[i - 1]).days == 1:
        if i - s0 > best_e - best_s:
            best_s, best_e = s0, i
    else:
        s0 = i
streak = list(range(best_s, best_e + 1))
streak_days  = [day_dt[i] for i in streak]
streak_hours = np.array([hours[i] for i in streak])

# ------------------------------------------------------------------ stats
def _g(t, c):
    nt, nc = len(t), len(c)
    sp = np.sqrt(((nt - 1) * t.var(ddof=1) + (nc - 1) * c.var(ddof=1)) / (nt + nc - 2))
    if sp == 0:
        return 0.0
    return (t.mean() - c.mean()) / sp * (1 - 3 / (4 * (nt + nc) - 9))

def hedges_g(test, control, nboot=5000, seed=7):
    rng = np.random.default_rng(seed)
    test, control = np.asarray(test, float), np.asarray(control, float)
    obs = _g(test, control)
    boots = np.array([_g(rng.choice(test, len(test)), rng.choice(control, len(control)))
                      for _ in range(nboot)])
    boots = np.clip(boots, -15, 15)  # tame tiny-n bootstrap blow-ups
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return dict(obs=obs, boots=boots, lo=lo, hi=hi)

def half_violin(ax, res, center, side, color, width=0.36, alpha=0.55, ci=True):
    b = res["boots"]
    kde = gaussian_kde(b)
    ys = np.linspace(b.min(), b.max(), 200)
    dens = kde(ys); dens = dens / dens.max() * width
    xs = center + dens if side == "right" else center - dens
    ax.fill_betweenx(ys, center, xs, color=color, alpha=alpha, lw=0, zorder=2)
    if ci:
        ax.plot([center, center], [res["lo"], res["hi"]], color=INK, lw=1.6, zorder=3)
    ax.plot(center, res["obs"], "o", color=INK, mfc="white", mew=1.4, ms=6, zorder=4)

def gapped_line(ax, x, vals, color=INK):
    """dabest-style mean +/- SD summary: a vertical line with a gap at the mean."""
    m = float(np.mean(vals)); sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    lo, hi = ax.get_ylim(); gap = 0.012 * (hi - lo)
    if sd == 0:
        ax.plot(x, m, "o", color=color, ms=4, zorder=6)
    else:
        ax.plot([x, x], [m - sd, m - gap], color=color, lw=2, zorder=6, solid_capstyle="butt")
        ax.plot([x, x], [m + gap, m + sd], color=color, lw=2, zorder=6, solid_capstyle="butt")

def swarm_x(n, center, spread=0.11, seed=3):
    return center + np.random.default_rng(seed).uniform(-spread, spread, n)

def clean(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color(AXISC); ax.spines["bottom"].set_color(AXISC)
    ax.tick_params(length=0); ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, lw=1); ax.xaxis.grid(False)

def ptitle(ax, letter, text):
    ax.set_title(f"{letter}   {text}", loc="left", color=INK, fontsize=12.5,
                 fontweight="bold", pad=8)

def month_day(dt):
    return f"{dt.strftime('%b')} {dt.day}"

# ================================================================== figure
fig = plt.figure(figsize=(13.5, 16.5), dpi=170)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(4, 2, height_ratios=[1.0, 1.7, 1.15, 0.32],
                      hspace=0.5, wspace=0.22,
                      left=0.075, right=0.965, top=0.925, bottom=0.05)
fig.suptitle("Focus Pocus  ·  a closer look at the numbers",
             color=NAVY, fontsize=20, fontweight="bold", x=0.075, ha="left", y=0.965)

# ---- A: hours per day, longest usage streak ----
axA = fig.add_subplot(gs[0, 0]); clean(axA)
xs = np.arange(len(streak))
axA.bar(xs, streak_hours, width=0.9, color=NAVY, lw=0, zorder=2)
axA.set_xlim(-0.6, len(xs) - 0.4); axA.set_ylim(0, 18)
axA.set_ylabel("Total hours (hr)")
tick_at = np.unique(np.linspace(0, len(xs) - 1, 5).round().astype(int))
axA.set_xticks(tick_at)
axA.set_xticklabels([month_day(streak_days[i]) for i in tick_at], fontsize=9)
axA.set_yticks([0, 6, 12, 18])
ptitle(axA, "A", f"Focus per day · longest streak ({len(xs)} days)")
pk = int(np.argmax(streak_hours))
axA.annotate(f"{streak_hours[pk]:.1f}hrs\nLongest working day",
             xy=(pk, streak_hours[pk]), xytext=(pk, streak_hours[pk] + 0.4),
             ha="center", va="bottom", fontsize=8.5, color=INK,
             fontweight="normal", linespacing=1.2)

# ---- C: efficiency by day (full range) ----
axC = fig.add_subplot(gs[0, 1]); clean(axC)
xnum   = mdates.date2num(day_dt)
c_meas = [np.mean(day_meas[d]) for d in days]
c_self = [np.mean(day_self[d]) if day_self[d] else np.nan for d in days]
axC.plot(xnum, c_meas, color=NAVY, lw=2, marker="o", ms=4, mfc=NAVY, mec="white",
         mew=0.7, label="Measured by the app", zorder=3)
axC.plot(xnum, c_self, color=GOLD, lw=2, ls=(0, (5, 3)), marker="s", ms=4, mfc=GOLD,
         mec="white", mew=0.7, label="My own rating", zorder=3)
axC.set_xlim(xnum[0] - 2, xnum[-1] + 2)
axC.set_ylim(0, 108); axC.set_yticks([0, 20, 40, 60, 80, 100])
axC.xaxis.set_major_locator(mdates.MonthLocator())
axC.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
axC.set_ylabel("% efficiency")
axC.legend(loc="lower left", frameon=False, fontsize=9, handlelength=1.6)
ptitle(axC, "C", "Efficiency by day")

# ---- B: dabest-style estimation, hours/day vs normal 8h ----
control_B = np.full(len(days), NORMAL_DAY_H)
gB = {i: hedges_g(np.array(wk_hours[i]), control_B, seed=10 + i) for i in range(7)}
groups = ["Normal\n(8h)"] + WK
gsB = gs[1, :].subgridspec(2, 1, height_ratios=[1.0, 0.85], hspace=0.06)
axBr = fig.add_subplot(gsB[0]); clean(axBr)
axBc = fig.add_subplot(gsB[1], sharex=axBr); clean(axBc)
axBr.set_ylim(0, 18)
# raw: swarm + dabest gapped mean/SD line offset to the right
axBr.scatter(swarm_x(len(days), 0, seed=1), control_B, s=13, color=MUTED, alpha=0.5, zorder=2)
gapped_line(axBr, 0.28, control_B, color=INK)
for i in range(7):
    vals = np.array(wk_hours[i])
    axBr.scatter(swarm_x(len(vals), i + 1, seed=20 + i), vals, s=15, color=NAVY, alpha=0.6, zorder=2)
    gapped_line(axBr, i + 1.28, vals, color=INK)
axBr.set_ylabel("Average hours per day")
plt.setp(axBr.get_xticklabels(), visible=False)
ptitle(axBr, "B", "Hours per day vs. a normal 8-hour workday")
# contrast: half-violins of Hedges' g
axBc.axhline(0, color=AXISC, lw=1, zorder=1)
for i in range(7):
    half_violin(axBc, gB[i], i + 1, "right", NAVY, width=0.34)
axBc.set_xlim(-0.6, 7.6); axBc.set_ylim(-6, 6)
axBc.set_xticks(range(8)); axBc.set_xticklabels(groups, fontsize=8.5)
axBc.set_ylabel("Hedges' g")

# ---- D: hours/session vs 25-min block (simplified: dots over violin) ----
gD = hedges_g(sess_hours, np.full(len(sess_hours), POMODORO_H), seed=42)
axD = fig.add_subplot(gs[2, 0]); clean(axD)
axD.set_xlim(0, 1); axD.set_xticks([])
half_violin(axD, gD, 0.32, "left", PBLUE, width=0.24, alpha=0.4, ci=False)
axD.set_ylabel("Hedges' g")
axD2 = axD.twinx()
axD2.scatter(swarm_x(len(sess_hours), 0.7, spread=0.09, seed=5), sess_hours,
             s=14, color=PGOLD, alpha=0.3, edgecolor="none", zorder=2)
axD2.plot(0.7, sess_hours.mean(), "o", color=INK, mfc="white", mew=1.3, ms=6, zorder=4)
axD2.axhline(POMODORO_H, color=GREY, ls=(0, (2, 2)), lw=1.1, zorder=1)
axD2.text(0.98, POMODORO_H, " 25-min ideal", color=GREY, fontsize=7.5, va="bottom", ha="right")
axD2.set_ylabel("Hours per session"); axD2.tick_params(length=0)
ptitle(axD, "D", "Hours per session vs. a 25-min block")

# ---- E: double half-violin, hours + efficiency effect sizes ----
gE_hours = hedges_g(hours, np.full(len(hours), NORMAL_DAY_H), seed=71)
gE_eff   = hedges_g(self_sess, meas_sess, seed=72)
axE = fig.add_subplot(gs[2, 1]); clean(axE)
axE.axhline(0, color=AXISC, lw=1, zorder=1)
half_violin(axE, gE_hours, 0.5, "left", NAVY, width=0.30)
half_violin(axE, gE_eff, 0.5, "right", GOLD, width=0.30)
axE.set_xlim(0, 1); axE.set_xticks([0.28, 0.72])
axE.set_xticklabels(["hours\nworked", "self\nefficiency"], fontsize=8.5)
axE.set_ylabel("Hedges' g")
ptitle(axE, "E", "Effect sizes: how far from 'normal'")

# ---- F: reserved ----
axF = fig.add_subplot(gs[3, :]); axF.axis("off")
axF.text(0.5, 0.5, "F  ·  reserved", ha="center", va="center",
         color=AXISC, fontsize=11, style="italic")

span = f"{day_dt[0].strftime('%b')} to {day_dt[-1].strftime('%b %Y')}"
footer = f"{len(sessions)} sessions  ·  {len(days)} days  ·  {hours.sum():.0f} h focused  ·  {span}"
if USING_SAMPLE:
    footer += "  ·  SAMPLE DATA"
fig.text(0.5, 0.02, footer, ha="center", color=MUTED, fontsize=10)

# NOTE: draft output goes to a separate file so it never clobbers the published
# figure (stats-dashboard.png). Rename to stats-dashboard.png only when finalised.
out = os.path.join(HERE, "stats-dashboard-DRAFT-SAMPLE.png" if USING_SAMPLE else "stats-dashboard-DRAFT.png")
fig.savefig(out, dpi=170, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
print("saved", out)
print(f"streak: {month_day(streak_days[0])}-{month_day(streak_days[-1])} ({len(streak)}d)")
print("B g: " + ", ".join(f"{WK[i]}={gB[i]['obs']:.2f}" for i in range(7)))
print(f"D g={gD['obs']:.2f}  E hours g={gE_hours['obs']:.2f}  E eff g={gE_eff['obs']:.2f}")
