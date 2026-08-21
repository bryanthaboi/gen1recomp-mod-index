# SaveSync

Play on the desktop, close it, open the game on your laptop, press CONTINUE —
your save is there. Sign in once and SaveSync looks after the rest.

Your saves live in free storage under your own account, so they stay yours to
take anywhere.

## Where your saves live

Pick one during setup. Each is free, and each keeps SaveSync to a single corner
of your account.

- **GitHub** — one secret gist, reached with the `gist` permission alone.
- **Dropbox** — one app folder of its own.
- **Your own server** — a small Docker container included in the repository,
  for anyone who would rather host it themselves.

Signing in on a second device finds the same storage by itself, so pairing is
just signing in again.

## Your progress is protected

- **If two devices changed the same save, it stops and asks you**, showing both
  — "here: 3 badges" against "cloud (Laptop): 5 badges" — so the choice stays
  yours.
- **Whichever you keep, the other survives.** Ten past versions live on the
  device and ten in the cloud, and every replacement keeps the outgoing save
  first.
- **CONTINUE speaks up** if it could not reach your cloud, tells you when you
  last synced, and lets you play anyway. Offline is a normal way to play.
- **Save files only.** The upload set is built by reading your save slots, so
  your saves are exactly what travels.

## Snapshots

Every five minutes SaveSync takes a snapshot — a copy of where you are, kept
beside your save, restorable from the menu. Your save file itself stays exactly
as you left it, so soft-resetting to re-roll a starter or a legendary works the
way it always has.

A plain auto-save that writes the real save file on a timer is there too, off
by default and yours to switch on.

## Install

1. Download `savesync-1.6.1.zip` from the releases page.
2. In the launcher, MODS → **Import mod .zip**, then enable **SaveSync**.
3. Title screen → **SAVESYNC** → Set Up → GitHub, and type the code it shows
   you on any device with a browser.

Repeat step 3 on your other devices.

## Permissions

`network` reaches your storage, `filesystem` keeps its own local backups, and
`engine_internals` reads and replaces save slots through the engine's own
`SaveData` — so the rules about where your progress lives stay in one place
rather than being reimplemented.

## Compatibility

Sits alongside other mods; it touches saves, not gameplay. Snapshots use the
engine's `mod.checkpoints` API and hide themselves on builds that predate it,
so everything else still works there.

MIT licensed. Original code and artwork throughout.
