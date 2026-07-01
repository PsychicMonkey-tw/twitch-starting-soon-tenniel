#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

USER="PsychicMonkey-tw"
REPO="twitch-starting-soon-tenniel"

echo "→ Вход в GitHub как ${USER}..."
if ! gh auth status 2>&1 | grep -q "account ${USER}"; then
  echo "Нужен вход в аккаунт ${USER}:"
  gh auth login -h github.com -p https -w
fi
gh auth setup-git

echo "→ Репозиторий..."
git remote set-url origin "https://github.com/${USER}/${REPO}.git"
if ! gh repo view "${USER}/${REPO}" >/dev/null 2>&1; then
  gh repo create "${REPO}" --public --source=. --remote=origin \
    --description "Tenniel Starting Soon — OBS, StreamElements, GitHub Pages"
fi

echo "→ Push..."
git push -u origin main

echo "→ GitHub Pages..."
gh api "repos/${USER}/${REPO}/pages" \
  -X POST -f 'build_type=legacy' -f 'source[branch]=main' -f 'source[path]=/docs' \
  2>/dev/null || gh api "repos/${USER}/${REPO}/pages" \
  -X PUT -f 'build_type=legacy' -f 'source[branch]=main' -f 'source[path]=/docs'

echo ""
echo "Готово!"
echo "  Репо:   https://github.com/${USER}/${REPO}"
echo "  OBS:    https://psychicmonkey-tw.github.io/${REPO}/"
echo "  SE:     streamelements/out/widget-github.json"
