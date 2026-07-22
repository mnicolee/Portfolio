# Private working TODO

Not published — the leading `_` makes Quarto skip it, so it never renders into the site.
Tracked in git so it syncs across devices. Shared scratchpad for Nicole + Claude —
say "bring up the todolist" any time.

## Open

- [ ] **DABEST page — apply the ChatGPT prose rewrite** (`papers/dabest/index.qmd`). Reverted to the
  old wording for now; the rewrite is staged in `_chatgpt-rewrite-bundle.md` (blocks `dabest.p1`–`p6`).
  Two things to resolve before applying:
  - The rewrite dropped a citation link: "acutely sensitive to sample size" → doi:10.1002/sim.2832.
    Decide where to reattach it (or drop it on purpose).
  - Old p5 walked through the figure "Panel a / b / c"; the rewrite is generic. Decide whether to keep
    explicit panel / Figure references.

- [ ] **Focus Pocus — fix the graphs** (badly done, especially the DABEST plots)

- [ ] **Blog post — DABEST then and now.** Write a post on who has been using the 2019 version of
  DABEST, and what the 2026 (DABEST 2.0) version brings to those users. Angle: profile the existing
  user base / use cases of the original, then lay out what's new in 2.0 and who it helps.

- [ ] **Contact — sort out the contact setup** (`contact.qmd`)
  - [ ] Create a Formspree form and replace `REPLACE_WITH_FORMSPREE_ID` with the real id
  - [ ] Decide/confirm which email it routes to (navbar mailto is `lnicole8282@gmail.com`)
  - [ ] Test that a submission actually lands in the inbox

## Done

- [x] **opn3 paper — ATR figure** — placed `atr-figure.jpg` between the two paragraphs of the
  "developmental retinal (ATR)" section, with `fig-alt` and a Nano Banana Pro credit line.
  Resized + converted from a 32 MB PNG down to a 308 KB / 1520px JPEG.

- [x] **Research card #1 title — de-specified to avoid being scooped** (`research.qmd`)
  - Now "Neural circuits of behavior in *Drosophila*" with a vaguer blurb (kept "ethomics"),
    dropping the internal-state/locomotion question and MBON split-GAL4 specifics.

