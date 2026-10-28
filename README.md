# cineticmotion.com — static site

Static rebuild of the Wix site for GitHub Pages. Korean pages at `/`, English at `/en/`.

## Layout
- `src/build.py` — all page text lives here; generates the `*.html` files and `sitemap.xml`.
- `assets/style.css`, `assets/site.js` — styling, mobile nav, form submit.
- `assets/img/` — images (see below).
- `scripts/fetch-assets.sh` — downloads the original images from the Wix CDN.

## Build
```bash
python3 src/build.py
```

## Images (one-time)
```bash
bash scripts/fetch-assets.sh
```
Requires normal internet access to `static.wixstatic.com` and ImageMagick (`convert`) for the 12 CM-1 feature icons.
Commit the downloaded files; the site does not reference Wix at runtime.

## Contact form
Wix Forms does not work on GitHub Pages. Create a free form at https://formspree.io, then replace
`YOUR_FORM_ID` in `src/build.py` (`FORM_ENDPOINT`) and rebuild. Until then the submit button shows an email prompt.

## Deploy
1. GitHub → Settings → Pages → Source: **GitHub Actions**. The workflow in `.github/workflows/pages.yml` deploys on every push to `main`.
2. Custom domain: add a `CNAME` file containing `www.cineticmotion.com`, then at the DNS provider point
   `www` CNAME → `<user>.github.io` and the apex A records → 185.199.108.153 / .109 / .110 / .111.
   Enable "Enforce HTTPS" in Pages settings once DNS resolves.
