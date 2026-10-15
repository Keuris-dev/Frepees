#!/data/data/com.termux/files/usr/bin/bash
# short.sh — buat shortlink via shrink.pe API
# usage: short.sh <url> [alias]
set -euo pipefail
KEY=$(cat "$HOME/.cuan/apikey.txt")
URL="${1:?usage: short.sh <url> [alias]}"
ALIAS="${2:-}"
Q="api=$KEY&url=$URL&format=text"
[ -n "$ALIAS" ] && Q="$Q&alias=$ALIAS"
curl -s -m 20 "https://shrink.pe/api?$Q"
echo
