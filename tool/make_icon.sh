#!/usr/bin/env bash
# Generates icon.png — the Marketplace gallery tile.
#
#   tool/make_icon.sh
#
# A prompt and a block cursor on the theme's own ground, in the theme's own
# mint, with the site's scanlines at the strength the portfolio uses. Nothing
# is invented: every value comes from the palette. Positions are explicit
# rather than gravity offsets, or the cursor welds onto the chevron and the
# whole thing reads as an arrow.
set -euo pipefail
cd "$(dirname "$0")/.."

BG="#050A08"; MINT="#3DDC97"
FONT="$HOME/Library/Fonts/3270-Regular.ttf"
[ -f "$FONT" ] || FONT="$HOME/Library/Fonts/VictorMono-Regular.ttf"

# 512 canvas. The pair sits on a common baseline, optically centred: the
# chevron is lighter than the solid block, so the group is nudged left of
# true centre to stop the block dragging it right.
CHEV_X=128 CHEV_Y=256
CUR_X0=278 CUR_Y0=176 CUR_X1=350 CUR_Y1=336

magick -size 512x512 xc:"$BG" \
  -font "$FONT" -pointsize 260 -fill "$MINT" \
  -gravity none -annotate +${CHEV_X}+330 ">" \
  -fill "$MINT" -draw "rectangle ${CUR_X0},${CUR_Y0} ${CUR_X1},${CUR_Y1}" \
  \( -size 512x512 xc:none -fill "#000000" \
     -draw "$(for y in $(seq 0 4 511); do printf 'rectangle 0,%s 511,%s ' "$y" "$y"; done)" \
     -alpha set -channel A -evaluate multiply 0.22 +channel \) -composite \
  icon-512.png

magick icon-512.png -resize 128x128 -strip icon.png
magick identify -format "  icon.png  %wx%h  %b\n" icon.png
magick identify -format "  icon-512  %wx%h  %b\n" icon-512.png
