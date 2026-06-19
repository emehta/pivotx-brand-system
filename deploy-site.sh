#!/usr/bin/env bash
# Deploy the marketing site (site/) to its live GitHub Pages repo: emehta/pivotx-site
# Live URL: https://emehta.github.io/pivotx-site/
#
# The site/ pages use ../fonts and ../assets (shared with the root brand deck).
# This flattens those to root-relative paths so the site can be the repo ROOT
# of the Pages deployment (clean URL, no /site/ subpath). Run after any site change.
#   ./deploy-site.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEPLOY="$(mktemp -d)/pivotx-deploy"
mkdir -p "$DEPLOY"

cp "$ROOT"/site/*.html "$ROOT"/site/styles.css "$ROOT"/site/app.js "$DEPLOY"/
cp -R "$ROOT/fonts"  "$DEPLOY/fonts"
cp -R "$ROOT/assets" "$DEPLOY/assets"
touch "$DEPLOY/.nojekyll"

# ../fonts/ and ../assets/ -> root-relative
sed -i '' 's#\.\./assets/#assets/#g' "$DEPLOY"/*.html
sed -i '' -e 's#\.\./fonts/#fonts/#g' -e 's#\.\./assets/#assets/#g' "$DEPLOY"/styles.css

cd "$DEPLOY"
git init -q -b main
git add -A
git -c user.email="eshaantm@gmail.com" -c user.name="Eshaan Mehta" commit -q -m "Deploy marketing site"
git remote add origin https://github.com/emehta/pivotx-site.git
git push -fq origin main
echo "Deployed -> https://emehta.github.io/pivotx-site/  (Pages rebuild takes ~30-60s)"
