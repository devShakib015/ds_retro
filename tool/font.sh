#!/usr/bin/env bash
# Switch the VS Code editor font while auditioning ds_retro.
#
#   tool/font.sh                 # list what is installed and what is active
#   tool/font.sh 3270            # switch to IBM 3270
#   tool/font.sh victor 15 1.8   # font, size, line height
#
# Backs up settings.json each time; restore with the newest .bak-* file.
set -euo pipefail
S="$HOME/Library/Application Support/Code/User/settings.json"

declare -a KEYS=(departure 3270 3270c victor share anon plex jetbrains fira)
family() { case "$1" in
  departure) echo "Departure Mono";;
  3270)      echo "IBM 3270";;
  3270c)     echo "IBM 3270 Semi-Condensed";;
  victor)    echo "Victor Mono";;
  share)     echo "Share Tech Mono";;
  anon)      echo "Anonymous Pro";;
  plex)      echo "IBM Plex Mono";;
  jetbrains) echo "JetBrains Mono";;
  fira)      echo "Fira Code";;
  *) echo "";; esac; }

if [ $# -eq 0 ]; then
  echo "installed candidates:"
  for k in "${KEYS[@]}"; do printf '  %-10s %s\n' "$k" "$(family "$k")"; done
  echo
  echo "active: $(python3 -c "import json,os;print(json.load(open(os.path.expanduser('$S')))['editor.fontFamily'])")"
  exit 0
fi

FAM=$(family "$1")
[ -z "$FAM" ] && { echo "unknown: $1"; exit 1; }
SIZE="${2:-15}"; LH="${3:-1.7}"
cp "$S" "$S.bak-$(date +%Y%m%d-%H%M%S)"
python3 - "$FAM" "$SIZE" "$LH" <<'PY'
import json, os, sys
fam, size, lh = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
p = os.path.expanduser("~/Library/Application Support/Code/User/settings.json")
d = json.load(open(p))
d["editor.fontFamily"] = f"{fam}, JetBrains Mono, monospace"
d["editor.fontSize"] = size
d["editor.lineHeight"] = lh
d["terminal.integrated.fontFamily"] = f"{fam}, monospace"
json.dump(d, open(p, "w"), indent=4)
print(f"  -> {fam}  {size}px  line-height {lh}")
PY
echo "  reload the window to see it (Cmd+Shift+P -> Developer: Reload Window)"
