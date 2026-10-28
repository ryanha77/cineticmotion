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

## Images / video
All 30 images are already committed in `assets/img/`. The only missing asset is the autoplay
background video on the home page (`assets/video/home-loop.mp4`, from `video.wixstatic.com`):
```bash
bash scripts/fetch-assets.sh   # re-downloads everything; needs ImageMagick for the CM-1 icon crops
python3 src/build.py           # the video section is emitted only once the mp4 exists
```
The site does not reference Wix at runtime.

## Contact form
GitHub Pages is static hosting: it cannot receive a POST, so a form needs an external endpoint.
- **Now (no setup):** the submit button opens the visitor's mail client (`mailto:info@cineticmotion.com`)
  with the filled-in fields as the message body.
- **Recommended:** create a free form at https://formspree.io (50 submissions/month free), replace
  `YOUR_FORM_ID` in `src/build.py` (`FORM_ENDPOINT`) and rebuild. Submissions then arrive by email
  without leaving the page. Alternatives with the same one-line swap: https://web3forms.com, https://getform.io.

## Analytics
Google Analytics 4 is wired into every page (`analytics()` in `src/build.py`).
1. In GA4: Admin → Data streams → Web → copy the Measurement ID (`G-…`).
2. Set `GA_ID` in `src/build.py` and rebuild. While it is the placeholder, no tag is emitted.
Tracked automatically: page views, `outbound_click` (Instagram etc.), `email_click`, `form_submit` (method: mailto/formspree), `form_error`.

## Deploy
1. GitHub → Settings → Pages → Source: **GitHub Actions**. The workflow in `.github/workflows/pages.yml` deploys on every push to `main`.
2. Custom domain: add a `CNAME` file containing `www.cineticmotion.com`, then at the DNS provider point
   `www` CNAME → `<user>.github.io` and the apex A records → 185.199.108.153 / .109 / .110 / .111.
   Enable "Enforce HTTPS" in Pages settings once DNS resolves.
