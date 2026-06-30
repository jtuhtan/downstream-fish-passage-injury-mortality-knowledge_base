<#
.SYNOPSIS
  Settle-aware commit / tag / push / release for the Downstream Fish Passage
  Injury & Mortality Knowledge Base.

.DESCRIPTION
  Run on demand or on a schedule. It encodes the project's git rhythm so the
  repository stays in sync as content evolves, without committing half-written
  files or ever publishing source PDFs:

    1. SETTLE  - if any file changed within -QuietMinutes, do nothing (avoids
                 committing files a parallel editor is still writing). Override
                 with -Force.
    2. GUARD   - refuses to commit any *.pdf (publisher copyright).
    3. COMMIT  - stages everything and commits with an auto-generated message.
    4. TAG     - if the top version in CHANGELOG.md has no matching git tag,
                 creates an annotated tag (a version bump is the deliberate
                 signal that a release is intended).
    5. PUSH    - pushes main and any new tag.
    6. RELEASE - for a new tag, creates a GitHub Release from that version's
                 CHANGELOG section (skip with -NoRelease).

  Requires: git and gh (authenticated). Windows PowerShell 5.1 compatible.

.NOTES
  OneDrive: keep OneDrive sync PAUSED during git operations. A live .git inside
  a synced folder can be locked/dehydrated by OneDrive and corrupted.

.EXAMPLE
  pwsh> .\scripts\sync_to_github.ps1            # settle-aware sync
  pwsh> .\scripts\sync_to_github.ps1 -Force     # sync now, ignore settle window
  pwsh> .\scripts\sync_to_github.ps1 -NoRelease # commit/tag/push, no GH release
#>
[CmdletBinding()]
param(
  [string]$RepoPath,
  [string]$RepoSlug    = 'jtuhtan/downstream-fish-passage-injury-mortality-knowledge_base',
  [int]   $QuietMinutes = 5,
  [switch]$Force,
  [switch]$NoRelease
)

$ErrorActionPreference = 'Stop'
if (-not $RepoPath) { $RepoPath = Split-Path $PSScriptRoot -Parent }
$LogPath = Join-Path $PSScriptRoot 'sync_to_github.log'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)  # PS5.1 Out-File utf8 adds a BOM; avoid it

function Log([string]$m) {
  $line = ("{0:yyyy-MM-dd HH:mm:ss}  {1}" -f (Get-Date), $m)
  Write-Output $line
  try { Add-Content -Path $LogPath -Value $line } catch {}
}

# Resolve gh (may not be on PATH in a scheduled-task session).
$gh = (Get-Command gh -ErrorAction SilentlyContinue).Source
if (-not $gh) { $c = 'C:\Program Files\GitHub CLI\gh.exe'; if (Test-Path $c) { $gh = $c } }

# 1. SETTLE -----------------------------------------------------------------
if (-not $Force) {
  $latest = Get-ChildItem -Recurse -File $RepoPath -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.Extension -ne '.log' } |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($latest -and ((Get-Date) - $latest.LastWriteTime).TotalMinutes -lt $QuietMinutes) {
    Log ("SKIP: not settled (last change '{0}' < {1} min ago)" -f $latest.Name, $QuietMinutes)
    return
  }
}

# 2/3. COMMIT (if dirty) ----------------------------------------------------
$dirty = git -C $RepoPath status --porcelain
if ($dirty) {
  git -C $RepoPath add -A
  $pdf = git -C $RepoPath diff --cached --name-only | Select-String -Pattern '\.pdf$'
  if ($pdf) {
    git -C $RepoPath reset -q
    Log ("ABORT: PDF staged - {0}" -f ($pdf -join ', '))
    throw "PDF guard tripped"
  }
  $names = git -C $RepoPath diff --cached --name-only
  $areas = ($names | ForEach-Object { ($_ -split '/')[0] } | Sort-Object -Unique) -join ', '
  $n     = ($names | Measure-Object -Line).Lines
  $msgFile = Join-Path $env:TEMP ("sync_msg_{0}.txt" -f ([guid]::NewGuid().ToString('N')))
  $msgText = @"
chore(sync): update $n file(s) [$areas]

Automated settle-aware sync of the knowledge base.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
"@
  [System.IO.File]::WriteAllText($msgFile, $msgText, $Utf8NoBom)
  git -C $RepoPath commit -q -F $msgFile
  Remove-Item $msgFile -ErrorAction SilentlyContinue
  Log ("COMMIT: {0} file(s) [{1}]" -f $n, $areas)
} else {
  Log "clean: no file changes"
}

# 4. VERSION-AWARE TAG ------------------------------------------------------
$ver = $null
foreach ($l in (Get-Content -Encoding UTF8 (Join-Path $RepoPath 'CHANGELOG.md'))) {
  if ($l -match '^\#\#\s*\[(\d+\.\d+\.\d+)\]') { $ver = $matches[1]; break }
}
$tag = $null
if ($ver) {
  $tag = "v$ver"
  if (-not (git -C $RepoPath tag --list $tag)) {
    git -C $RepoPath tag -a $tag -m $tag
    Log ("TAG: {0}" -f $tag)
  }
}

# 5. PUSH (retry transient failures; abort LOUDLY on real failure) ----------
function Push-WithRetry([string[]]$pushArgs, [string]$what) {
  for ($i = 1; $i -le 3; $i++) {
    git -C $RepoPath @pushArgs
    if ($LASTEXITCODE -eq 0) { return $true }
    Log ("WARN: push of {0} failed (exit {1}); attempt {2}/3" -f $what, $LASTEXITCODE, $i)
    Start-Sleep 6
  }
  return $false
}
if (-not (Push-WithRetry @('push', 'origin', 'HEAD') 'main')) {
  Log "ERROR: could not push main. Commit + tag are saved LOCALLY; fix connectivity and re-run (this script is idempotent)."
  throw "git push (main) failed"
}
if ($tag) {
  # pushing an already-present tag is a harmless no-op, so this is safe on re-run
  if (-not (Push-WithRetry @('push', 'origin', $tag) $tag)) {
    Log ("ERROR: main pushed but tag {0} did not; re-run to finish tag + release." -f $tag)
    throw "git push (tag) failed"
  }
}
Log ("PUSH: main{0}" -f $(if ($tag) { " + $tag" } else { "" }))

# 6. RELEASE (idempotent: only create if it does not already exist) ----------
if ($tag -and -not $NoRelease -and $gh) {
  # Does the release already exist? Toggle ErrorActionPreference so the native
  # stderr from `gh release view` on a not-found release isn't wrapped into a
  # terminating error (PS 5.1 trap) — we only want its exit code.
  $eapSaved = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'
  & $gh release view $tag --repo $RepoSlug --json tagName 1>$null 2>$null
  $relMissing = ($LASTEXITCODE -ne 0)
  $ErrorActionPreference = $eapSaved
  if ($relMissing) {
    $notes = New-Object System.Collections.Generic.List[string]
    $inSec = $false
    foreach ($l in (Get-Content -Encoding UTF8 (Join-Path $RepoPath 'CHANGELOG.md'))) {
      if ($l -match '^\#\#\s*\[') {
        if ($inSec) { break }
        if ($l -match ("\[{0}\]" -f [regex]::Escape($ver))) { $inSec = $true; continue }
      }
      if ($inSec) { $notes.Add($l) }
    }
    $nf = Join-Path $env:TEMP ("relnotes_{0}.md" -f $ver)
    [System.IO.File]::WriteAllText($nf, ($notes -join "`n").Trim(), $Utf8NoBom)
    & $gh release create $tag --repo $RepoSlug --title $tag --notes-file $nf --verify-tag
    if ($LASTEXITCODE -eq 0) { Log ("RELEASE: {0}" -f $tag) }
    else { Log ("ERROR: release create for {0} failed (exit {1})" -f $tag, $LASTEXITCODE) }
    Remove-Item $nf -ErrorAction SilentlyContinue
  } else {
    Log ("RELEASE: {0} already exists, skipping" -f $tag)
  }
}

Log "done"
