# Private working TODO

Not published — the leading `_` makes Quarto skip it, so it never renders into the site.
Tracked in git so it syncs across devices. Shared scratchpad for Nicole + Claude —
say "bring up the todolist" any time.

## Open

- [ ] **"Inside the Black Box" is LIVE** (`musings/ai-bootcamp/index.qmd`), the first musings post.
  Three figures alongside it as transparent SVG. Every factual claim was checked against primary
  sources. Three things still open, none blocking:
  - The date. The opening still says "last month" rather than the actual bootcamp dates.
  - Two references: the Waddell year and journal (Trends in Neurosciences 2010 vs Curr Opin
    Neurobiol 2013), and which of the two Aso 2014 eLife papers is cited where (e04577 is the
    anatomy one, e04580 is output neurons encode valence).
  - `fig3-naming.svg` is orphaned in the folder; it belonged to a section that was cut. Delete it
    or reuse it.
  - Known trap, already handled but do not undo it: cite Felsenberg 2018, **not** Perisse 2016,
    for MBON-γ1pedc>α/β inhibiting MBON-γ5β'2a. Perisse measured a pooled population and reports
    no overlap at that cell.
  - Figure conventions: warm colours are neuroscience, teal is reserved for AI vocabulary. The
    SVGs carry literal hex, not CSS variables, so they survive being moved.

- [ ] **DABEST page — prose rewrite** (`papers/dabest/index.qmd`). Currently on the old wording.
  NOTE: `_chatgpt-rewrite-bundle.md` was deleted on 2026-07-26; it never actually contained the
  DABEST blocks (its own header excluded that page), so the rewrite it referred to does not exist
  in this repo. Redo it from scratch if you still want it. Two things to resolve either way:
  - A previous rewrite dropped a citation link: "acutely sensitive to sample size" →
    doi:10.1002/sim.2832. Decide where to reattach it, or drop it on purpose.
  - The old p5 walked through the figure "Panel a / b / c". Decide whether to keep explicit
    panel and figure references or go generic.

## House style for prose

Kept from the deleted rewrite bundle, because it is the only place these were written down:
sound like a real, warm person, not AI. Keep all facts, names, numbers, links, and the existing
**bold** / *italic* emphasis. No em dashes. No "notable". Not peppy, not salesy. Similar length
or slightly shorter.

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

