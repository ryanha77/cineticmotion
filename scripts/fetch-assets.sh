#!/usr/bin/env bash
# Downloads the original images from the current Wix site into assets/img/.
# Run from the repo root on a machine with normal internet access:  bash scripts/fetch-assets.sh
# Note: Wix serves originals at static.wixstatic.com/media/<id>. Sprite sheets (cm1 icons) are cropped with ImageMagick if available.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=assets/img; mkdir -p "$OUT"
B="https://static.wixstatic.com/media"
get(){ echo "  $2"; curl -fsSL "$B/$1" -o "$OUT/$2"; }
get "d14da8_8432b74955b04714b91a0779dfab751c~mv2.png"  logo-white.png
get "81af6121f84c41a5b4391d7d37fce12a.png"               instagram.png
get "d14da8_871e7e5704a94b3095f01279e39597a7~mv2.png"  favicon.png
# Home (the second home section is an autoplay background video on Wix; 720p = 9 MB, 1080p = 20 MB - swap the path if you want 1080p)
mkdir -p assets/video
echo "  assets/video/home-loop.mp4"; curl -fsSL "https://video.wixstatic.com/video/d14da8_dc1c8b6c23c84d1a8bf84b5603abd6a4/720p/mp4/file.mp4" -o assets/video/home-loop.mp4 || echo "  (video download failed - rerun later; the section is skipped at build time while the file is missing)"
get "d14da8_8facba4b2ab24c6e9355beb9724d0a14~mv2.jpg"  home-hero.jpg
# Products
get "ae1c23_a6e35c6827304afe8c30fac04f93b774~mv2.png"  cm1-wordmark.png
get "ae1c23_6694b1c15c274942a2f0dab19c538e21~mv2.png"  radius-wordmark.png
get "ae1c23_e6145c60c41e48168f589bd909cf8f89~mv2.jpg"  products-cm1.jpg      # "bg_2" set photo (CM-1 column on Wix)
get "ae1c23_e576433298a842bcad41fdfa4d1369d8~mv2.jpg"  products-radius.jpg   # "RADIUS INTERFACE" (RADIUS column on Wix)
get "d14da8_2e850572e55747e3af49c66a4c5d79aa~mv2.jpg"  products-bg.jpg
# CM-1
get "d14da8_03ad5ee4f761400ba5c8c7e77b2f6f71~mv2.jpg"  cm1-bg.jpg
get "d14da8_86139ef3e79949c3b59ab119bbc035eb~mv2.png"  cm1-hero.png   # converted to cm1-hero.jpg (1600px) in the repo
get "d14da8_efa4ae8cbfbf432685477a26d8f92d06~mv2.jpg"  cm1-features-bg.jpg
get "d14da8_466396a5758d4b658d55a1c6c6c42819~mv2.png"  cm1-title.png
get "ae1c23_60e79afa41584f1792d90a164751e824~mv2.png"  cm1-product.png
get "d14da8_a0748d1cec104de2bfd29458033aea03~mv2.png"  cm1-sprite-a.png
get "d14da8_aa4d211d16374c499ef078f393cedfc6~mv2.png"  cm1-sprite-b.png
get "d14da8_e56648e51cfa4ba9b37affc3b4d169c1~mv2.png"  cm1-sprite-c.png
# RADIUS
get "d14da8_d165304fc7f04e63be1180ea23012414~mv2.jpg"  radius-hero.jpg
get "d14da8_48c4510fdb914975bedbd84caa54d42d~mv2.png"  radius-title.png
get "ae1c23_10c2f062092941278aebf5222fdbba4d~mv2.png"  radius-product.png
get "ae1c23_2d69ccd5bc7741c28122a4f07d8e8bb9~mv2.png"  radius-screen.png
# RADIUS key-feature images, in page order, with the crop geometry used on the Wix page
i=1; while read -r id geom; do
  get "$id~mv2.jpg" "radius-feature-$i.jpg"
  command -v convert >/dev/null && convert "$OUT/radius-feature-$i.jpg" -crop "$geom" +repage "$OUT/radius-feature-$i.jpg"
  i=$((i+1))
done <<'LIST'
ae1c23_a0f79af3b4164e8882c44551a4435e5d 807x1335+112+0
ae1c23_087f2bb76d9e4eb1b7d4c54eda85726e 757x1254+249+0
ae1c23_a2cb44496b184709a1ffe0b700312ec5 387x639+145+0
ae1c23_dfadf20efef7450fa98ff6ecfe6d7cb9 254x414+0+225
ae1c23_df316c806335497da32164fc298164b6 392x639+14+0
ae1c23_63c5379b1b0b44f2ae1cd058c8b0b998 393x639+70+0
LIST
# CM-1 feature icons: 4 crops per sprite sheet (crop geometry taken from the Wix page)
if command -v convert >/dev/null; then
  n=1
  for g in "401x489+0+0" "403x491+567+0" "403x491+1095+0" "378x491+1626+0"; do convert "$OUT/cm1-sprite-a.png" -crop "$g" +repage "$OUT/cm1-icon-$(printf %02d $n).png"; n=$((n+1)); done
  for g in "380x443+19+0" "343x443+588+0" "343x443+1132+0" "343x443+1661+0"; do convert "$OUT/cm1-sprite-b.png" -crop "$g" +repage "$OUT/cm1-icon-$(printf %02d $n).png"; n=$((n+1)); done
  for g in "341x542+0+0" "341x542+559+0" "360x542+1113+0" "341x514+1663+28"; do convert "$OUT/cm1-sprite-c.png" -crop "$g" +repage "$OUT/cm1-icon-$(printf %02d $n).png"; n=$((n+1)); done
else echo "ImageMagick not found: cm1-icon-XX.png not generated (crop cm1-sprite-*.png manually)"; fi
rm -f "$OUT"/cm1-sprite-*.png
echo done
