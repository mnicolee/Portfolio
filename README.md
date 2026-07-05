# Nicole M. Lee — portfolio

**Site → <https://lnicole08.github.io/Portfolio/>**

The personal portfolio of Nicole M. Lee, PhD — a behavioral neuroscientist working on
optogenetic silencing tools, custom behavior-tracking hardware, and estimation statistics.
Built with [Quarto](https://quarto.org) and deployed to GitHub Pages.

---

## Local preview

```bash
quarto preview
```

Live-reloading preview; edit a `.qmd` and save to refresh.

## Deploy

Every push to `main` rebuilds the site and publishes to the `gh-pages` branch via
`.github/workflows/publish.yml`. One-time on GitHub: **Settings → Pages → Source =
`gh-pages` / `(root)`**.

## To do

- [ ] Enable GitHub Pages (Settings → Pages → `gh-pages`) so the site above goes live.
- [ ] Contact form: create a dedicated email, sign up at [formspree.io](https://formspree.io),
      and put the form ID into `contact.qmd` (replacing `REPLACE_WITH_FORMSPREE_ID`).
