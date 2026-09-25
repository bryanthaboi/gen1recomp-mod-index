# Mod scanning and local review

The scanner uses source inspection and a fixed reference snapshot. It never executes mod code. Exact RGBA pixel hashes are separate from 256 bit perceptual similarity. Similarity is not a legal conclusion. The default policy automatically quarantines strong console signatures or 25 distinct exact assets; 100 distinct similarity matches trigger priority review. Duplicate files do not inflate these counts. Tune `policy.json` and rebuild both images to change policy.

The dependency-free API analyzer and image comparison routines were extracted from the supplied scanner archive. See `UPSTREAM.md`. Cart bundles and pinned dependencies are scanned. Unreadable sources, resource limits, nested archives and parser failures produce incomplete results, not clean passes. API warnings remain advisory; definite API errors block PR checks and release publication.

## Local service

Open http://localhost:8849 on the installed machine. The dashboard lists current results, evidence previews, full findings, and scan history. Approve, quarantine and reset decisions apply to an archive SHA256. Approval never turns an incomplete scan into a pass. A later release is evaluated independently. The database and reference images stay under the user's private Application Support directory, outside this repository. SQLite WAL state lives in the local Docker volume `gen1mod-review-db` so database locks stay on the Linux filesystem. Each completed audit also writes a consistent SQLite backup to the private `state/backups` directory. Preserve both the database volume and the private state directory when updating or uninstalling.

The container restarts automatically while Docker is running. A macOS LaunchAgent starts the runner supervisor at login and retries when Docker becomes available. Docker Desktop must be running; sleeping or powered-off machines catch up after they resume. The service schedules one full catalog scan per local calendar day at midnight in America/New_York, with startup catch-up, and a digest after 08:00. Buttons allow manual rescans and publication retries. The UI is loopback-only, uses Host validation and CSRF form tokens, and does not expose a remote administration port.

Priority Pushcut alerts include counts, grouped notification identifiers and a comparison image when available. A durable outbox retries failures and deduplicates identical findings. Ordinary changes enter a morning digest. Pushcut dynamic payloads require Pro. Phone alerts link to GitHub by default because localhost on a phone is not this machine. A private remote URL requires a separate authenticated access setup; no public tunnel is installed.

## GitHub integration

`PUSHCUT_WEBHOOK_URL` is a repository Actions secret. A trusted GitHub-hosted workflow sends PR failure notifications after the scan workflow finishes; the scan runner never receives it. The local notification service reads a separate protected local credential file.

PR scans use a disposable Linux ARM64 runner with the `mod-scan` label. The host supervisor requests a short-lived registration token for each fresh container, and GitHub deregisters it after one job. Jobs have no Docker socket, host home directory, moderation database, GitHub write credential, or Pushcut credential. Only reference images and the trusted scan-result cache are mounted read-only. Paths in jobs are `/workspace`, `/opt/scanner`, `/references` and `/scan-cache`; reports redact host home paths and secret patterns.

The trusted local controller writes `.health/moderation.json` on main when quarantine decisions change. The index builder omits those entries but preserves their original metadata for restoration. An incomplete rescan retains previous quarantine. Pages scans the exact resolved release archives before publication and omits incomplete, quarantined or API-invalid entries; a widespread incomplete-scan outage aborts deployment to preserve the previous site. Every Pages rebuild passes through this gate, including cleanup-triggered rebuilds.

Reports are saved as `mod-scan-report` workflow artifacts and imported into local history every five minutes as untrusted CI evidence. Only the trusted local scan and explicit local decisions change quarantine state. Cached results require the downloaded archive SHA256 and the scanner, configuration and reference revision. No approval is cached by URL or version alone.

## Installation and updates

The repository contains no credentials or reference image pixels. Install the reference images in the private installation directory, then build `references.json` with `cli.py --build-references IMAGES OUTPUT`. Provision protected local `secrets/github-token` and `secrets/pushcut-url` files there. The GitHub credential needs repository contents write for moderation updates; runner registration uses the host's existing `gh` keychain authentication. Run `python3 scanner/install-local.py` to build/install or update. Existing database and decisions survive updates. The current Docker runner definition targets ARM64 and pins the official runner archive checksum.

After code or policy changes, rebuild with the installer so the installed trusted scanner and CI use the same revision. The workflow deliberately runs `/opt/scanner/cli.py`, not scanner code supplied by a PR. References are fixed until explicitly regenerated. Keep the API rules aligned with the engine; this release retains the upstream regex analyzer's known limitations around complex Lua syntax.

Tests: `python -m unittest discover -s scanner/tests` with `PYTHONPATH=scanner`, and `node --test scripts/moderation.test.mjs`. Full index tests run with `node --test scripts/test.mjs`.

To stop: unload `org.gen1recomp.mod-review` with launchctl, stop the `gen1mod-review` container, and stop any `mod-scan-*` container. Preserve the private state directory to retain moderation history.
