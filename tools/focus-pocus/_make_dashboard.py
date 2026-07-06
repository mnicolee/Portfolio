import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

# ---- brand palette (from theme-light.scss) ----
NAVY   = "#1E3A6E"   # objective / measured by the app
GOLD   = "#C29B2E"   # subjective / your own self-rating
INK    = "#1C2433"
MUTED  = "#8A8272"
GRID   = "#ECE7DA"
AXISC  = "#C9C0AD"
BG     = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": AXISC,
})

def rbar(ax, x, h, w, color, rmax=None):
    """A clean flush bar anchored at the baseline."""
    if h <= 0:
        return
    ax.bar(x, h, width=w, color=color, linewidth=0, zorder=2)

def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(AXISC)
    ax.spines["bottom"].set_color(AXISC)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, lw=1)
    ax.xaxis.grid(False)

# ------------------------------------------------------------------ data
# NOTE: transcribed from the previous stats-dashboard.png — replace with a
# real session export for exact values.
hours = [1.2,3.6,4.0,4.2,7.6,6.4,1.4,6.6,5.0,2.3,
         10.6,9.4,5.2,5.5,7.1,5.4,3.9,6.2,2.1,1.3]
peak = int(np.argmax(hours))

measured = [88,100,100,100,100,100,100,100,98,100,92,100,95,100,
            100,93,100,100,100,100,100,100,100,100,100,100,100,92]
selfeff  = [np.nan]*7 + [76,86,89,77,84,91,76,82,71,79,65,68,79,79,
                         89,82,94,74,92,88,68]

wk_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
wk_counts = [1,2,8,5,3,3,6]
busiest = int(np.argmax(wk_counts))

s_vals = np.array([v for v in selfeff if not np.isnan(v)])
bins = np.arange(60, 101, 5)
mean_self = float(np.nanmean(s_vals))

# ------------------------------------------------------------------ figure
fig, axs = plt.subplots(2, 2, figsize=(12, 8.3), dpi=200)
fig.subplots_adjust(left=0.065, right=0.975, top=0.83, bottom=0.10,
                    hspace=0.42, wspace=0.20)

fig.suptitle("Focus Pocus  ·  a month of focus, at a glance",
             color=NAVY, fontsize=21, fontweight="bold", y=0.965)
fig.text(0.5, 0.905,
         "Navy = measured by the app        Gold = my own self-rating",
         ha="center", color=MUTED, fontsize=12.5)

# ---- Panel A: focus time per day (objective -> navy) ----
axA = axs[0, 0]; clean(axA)
for i, h in enumerate(hours):
    rbar(axA, i, h, 0.80, NAVY, rmax=0.35)
axA.set_xlim(-0.7, len(hours)-0.3); axA.set_ylim(0, 12)
axA.set_title("Focus time per day", loc="left", color=INK,
              fontsize=14, fontweight="bold", pad=8)
axA.set_ylabel("hours")
ticks = [0, 5, 10, 15, 19]
axA.set_xticks(ticks)
axA.set_xticklabels(["Jan 3","Jan 9","Jan 29","Feb 6","Feb 14"], fontsize=9.5)
axA.set_yticks([0,3,6,9,12])
axA.annotate(f"{hours[peak]:.1f} h\nbest day", xy=(peak, hours[peak]),
             xytext=(peak, hours[peak]+0.55), ha="center", va="bottom",
             fontsize=9.5, color=INK, fontweight="bold", linespacing=1.15)

# ---- Panel B: measured vs self-assessed efficiency (the anchor) ----
axB = axs[0, 1]; clean(axB)
x = np.arange(len(measured))
axB.plot(x, measured, color=NAVY, lw=2.2, marker="o", ms=5.5,
         mfc=NAVY, mec="white", mew=0.8, zorder=3, label="Measured by the app")
axB.plot(x, selfeff, color=GOLD, lw=2.2, ls=(0,(5,3)), marker="s", ms=5.5,
         mfc=GOLD, mec="white", mew=0.8, zorder=3, label="My own rating")
axB.set_ylim(0, 108); axB.set_yticks([0,20,40,60,80,100])
axB.set_xlim(-0.6, len(x)-0.4)
axB.set_title("Measured vs. self-assessed efficiency", loc="left",
              color=INK, fontsize=14, fontweight="bold", pad=8)
axB.set_ylabel("% efficiency"); axB.set_xlabel("session", fontsize=10)
axB.set_xticks([0,7,14,21,27])
axB.legend(loc="lower left", frameon=False, fontsize=10.5,
           handlelength=1.8, borderaxespad=0.3)

# ---- Panel C: sessions by weekday (objective -> navy) ----
axC = axs[1, 0]; clean(axC)
for i, c in enumerate(wk_counts):
    rbar(axC, i, c, 0.72, NAVY, rmax=0.28)
axC.set_xlim(-0.7, 6.7); axC.set_ylim(0, 9)
axC.set_xticks(range(7)); axC.set_xticklabels(wk_labels, fontsize=10.5)
axC.set_yticks([0,2,4,6,8])
axC.set_title("When you show up  ·  sessions by weekday", loc="left",
              color=INK, fontsize=14, fontweight="bold", pad=8)
axC.set_ylabel("sessions")
axC.annotate("busiest", xy=(busiest, wk_counts[busiest]),
             xytext=(busiest, wk_counts[busiest]+0.35), ha="center",
             va="bottom", fontsize=9.5, color=INK, fontweight="bold")

# ---- Panel D: how you rated yourself (subjective -> gold) ----
axD = axs[1, 1]; clean(axD)
counts, edges = np.histogram(s_vals, bins=bins)
for c, lo, hi in zip(counts, edges[:-1], edges[1:]):
    if c > 0:
        rbar(axD, (lo+hi)/2, c, (hi-lo)*0.82, GOLD, rmax=1.2)
axD.axvline(mean_self, color=INK, ls=(0,(4,3)), lw=1.6, zorder=4)
axD.text(mean_self+0.6, counts.max()*0.96, f"mean {mean_self:.0f}%",
         color=INK, fontsize=10.5, fontweight="bold", va="top")
axD.set_xlim(60, 100); axD.set_ylim(0, counts.max()+1)
axD.set_xticks([60,65,70,75,80,85,90,95,100])
axD.set_yticks(range(0, counts.max()+2))
axD.set_title("How you rated yourself", loc="left", color=INK,
              fontsize=14, fontweight="bold", pad=8)
axD.set_ylabel("sessions"); axD.set_xlabel("self-assessed efficiency (%)")

fig.text(0.5, 0.028,
         "28 sessions  ·  20 days  ·  96 h focused  ·  Jan–Mar 2026",
         ha="center", color=MUTED, fontsize=11)

out = r"C:\Users\User\Documents\GitHub\Portfolio\tools\focus-pocus\stats-dashboard.png"
fig.savefig(out, dpi=200, facecolor=BG, bbox_inches="tight", pad_inches=0.25)
print("saved", out)
print("mean_self", round(mean_self,1), "| hist", counts.tolist(),
      "| sum", int(counts.sum()))
