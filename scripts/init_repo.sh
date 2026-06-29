#!/usr/bin/env bash
# One-time setup: run this ON YOUR MACHINE from the repo root to create the git
# repo and push it to GitHub. (git could not be initialised from the sandbox
# because OneDrive locks git's internal lockfiles.)
set -e
git init
git branch -M main
git add -A
# Safety: confirm no PDFs are about to be committed
if git ls-files | grep -qi '\.pdf$'; then echo "ABORT: PDFs staged — check .gitignore"; exit 1; fi
git commit -m "Initial release (v0.1.0): structured review, barotrauma reproducibility assessment, methodology & skill"
# Create the empty repo on GitHub first (UI or: gh repo create jtuhtan/downstream-fish-passage-injury-mortality-kb --public --source=. --remote=origin)
git remote add origin https://github.com/jtuhtan/downstream-fish-passage-injury-mortality-kb.git
git push -u origin main
