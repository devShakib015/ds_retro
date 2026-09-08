#!/usr/bin/env bash
# Installs the coding fonts ds_retro is designed against.
#
#   tool/install-fonts.sh            # the recommended one (Victor Mono)
#   tool/install-fonts.sh --all      # every candidate, to audition with tool/font.sh
#
# VS Code Settings Sync carries editor.fontFamily but NOT the font itself —
# fonts are an OS install. So a synced machine renders the fallback until this
# has been run there too. Idempotent: already-installed faces are skipped.
set -euo pipefail

case "$(uname -s)" in
  Darwin) DEST="$HOME/Library/Fonts" ;;
  Linux)  DEST="$HOME/.local/share/fonts" ;;
  *) echo "unsupported platform: $(uname -s)"; exit 1 ;;
esac
mkdir -p "$DEST"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
ALL=${1:-}

have() { ls "$DEST" 2>/dev/null | grep -qi "^$1"; }
say()  { printf '  %-22s %s\n' "$1" "$2"; }

# --- Victor Mono — the one the theme is designed against ---------------------
# Its italics are cursive, and comments, keywords, this, parameters and
# annotations are all italic in ds_retro, so the face does half the work.
if have "VictorMono"; then say "Victor Mono" "already installed"; else
  curl -sfL --max-time 300 -o "$TMP/victor.zip" "https://rubjo.github.io/victor-mono/VictorMonoAll.zip" \
    && unzip -oq "$TMP/victor.zip" -d "$TMP/victor" \
    && find "$TMP/victor/TTF" -name "VictorMono-Regular.ttf" -o -name "VictorMono-Italic.ttf" \
         -o -name "VictorMono-Bold.ttf" -o -name "VictorMono-BoldItalic.ttf" \
       | xargs -I{} cp {} "$DEST/" \
    && say "Victor Mono" "installed" || say "Victor Mono" "FAILED"
fi

[ "$ALL" = "--all" ] || { echo; echo "  done. --all adds the other candidates."; exit 0; }

# --- IBM 3270 — the literal mainframe terminal -------------------------------
if have "3270"; then say "IBM 3270" "already installed"; else
  U=$(curl -s https://api.github.com/repos/rbanffy/3270font/releases/latest \
      | python3 -c "import json,sys;print(next((a['browser_download_url'] for a in json.load(sys.stdin)['assets'] if a['name'].endswith('.zip')),''))")
  [ -n "$U" ] && curl -sfL --max-time 300 -o "$TMP/3270.zip" "$U" && unzip -oq "$TMP/3270.zip" -d "$TMP/3270" \
    && find "$TMP/3270" -name "3270-Regular.ttf" -o -name "3270SemiCondensed-Regular.ttf" \
       | grep -iv nerd | xargs -I{} cp {} "$DEST/" \
    && say "IBM 3270" "installed" || say "IBM 3270" "FAILED"
fi

# --- Departure Mono — pixel/CRT, Regular only --------------------------------
if have "DepartureMono"; then say "Departure Mono" "already installed"; else
  U=$(curl -s https://api.github.com/repos/rektdeckard/departure-mono/releases/latest \
      | python3 -c "import json,sys;print(next((a['browser_download_url'] for a in json.load(sys.stdin)['assets'] if a['name'].endswith('.zip')),''))")
  [ -n "$U" ] && curl -sfL --max-time 300 -o "$TMP/dep.zip" "$U" && unzip -oq "$TMP/dep.zip" -d "$TMP/dep" \
    && find "$TMP/dep" -name "*.otf" | xargs -I{} cp {} "$DEST/" \
    && say "Departure Mono" "installed" || say "Departure Mono" "FAILED"
fi

# --- The rest, single files ---------------------------------------------------
GF="https://raw.githubusercontent.com/google/fonts/main/ofl"
one() { # name, filename, url
  if have "$2"; then say "$1" "already installed"; return; fi
  curl -sfL --max-time 180 -o "$DEST/$2" "$3" && say "$1" "installed" || { rm -f "$DEST/$2"; say "$1" "FAILED"; }
}
one "Share Tech Mono" "ShareTechMono-Regular.ttf" "$GF/sharetechmono/ShareTechMono-Regular.ttf"
one "Anonymous Pro"   "AnonymousPro-Regular.ttf"  "$GF/anonymouspro/AnonymousPro-Regular.ttf"
one "Anonymous Pro I" "AnonymousPro-Italic.ttf"   "$GF/anonymouspro/AnonymousPro-Italic.ttf"
one "IBM Plex Mono"   "IBMPlexMono-Regular.ttf" \
  "https://github.com/IBM/plex/raw/master/packages/plex-mono/fonts/complete/ttf/IBMPlexMono-Regular.ttf"
one "JetBrains Mono"  "JetBrainsMono-Regular.ttf" \
  "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Regular.ttf"
one "JetBrains Mono B" "JetBrainsMono-Bold.ttf" \
  "https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/fonts/ttf/JetBrainsMono-Bold.ttf"

echo
echo "  done -> $DEST"
