# Private working TODO

Not published — the leading `_` makes Quarto skip it, so it never renders into the site.
Tracked in git so it syncs across devices. Shared scratchpad for Nicole + Claude —
say "bring up the todolist" any time.

## Open

- [ ] **opn3 paper — ATR figure** (`papers/opn3/index.qmd`, in the "developmental retinal (ATR)" section)
  - [ ] Add the image file to `papers/opn3/` (e.g. `atr-figure.png`)
  - [ ] Insert the figure after that section's paragraph; set filename + real `fig-alt`:
    `![](atr-figure.png){.paper-figure style="max-width:760px" fig-alt="..."}`
  - [ ] Add the caption / figure credit line:
    `[caption / credit]{.figure-credit style="max-width:760px"}`
  - Blocked on: the figure image being supplied.

- [ ] **Focus Pocus — fix the graphs** (badly done, especially the DABEST plots)

- [ ] **Contact — sort out the contact setup** (`contact.qmd`)
  - [ ] Create a Formspree form and replace `REPLACE_WITH_FORMSPREE_ID` with the real id
  - [ ] Decide/confirm which email it routes to (navbar mailto is `lnicole8282@gmail.com`)
  - [ ] Test that a submission actually lands in the inbox

- [ ] **Revisit the bolding** across research / hardware / tools pages
  - Re-read each page and reconsider what's bolded — confirm each bold is the right "one key point"
    and nothing is over- or under-bolded.

- [ ] **Figure/image zoom (lightbox)** — clicking a figure/image should blow it up / bring it into
  focus (zoom-to-fill overlay), then click again or Esc to close. Applies to `.paper-figure`,
  `.graphical-abstract`, and figures inside the paper/hardware pages.

## Done

- [x] **Research card #1 title — de-specified to avoid being scooped** (`research.qmd`)
  - Now "Neural circuits of behavior in *Drosophila*" with a vaguer blurb (kept "ethomics"),
    dropping the internal-state/locomotion question and MBON split-GAL4 specifics.

