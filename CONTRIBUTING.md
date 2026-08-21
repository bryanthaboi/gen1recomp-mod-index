# Submitting a mod

## The easy way

Open the [submission helper](https://bryanthaboi.github.io/gen1recomp-mod-index/),
fill in the form, sign in with GitHub, press **Open pull request**. The page
forks this repo to your account, commits `mods/<Author>@<id>/`, and opens the
PR. It validates against the same schema CI does, so if the form is happy the
build usually is too.

No account, or you would rather not hand a token to a web page? The same page's
**Submit by hand** button gives you prefilled github.com links, and the layout
below is all you actually need.

## The manual way

Add one folder:

```
mods/<Author>@<mod id>/
  meta.json
  description.md
  thumbnail.png      (optional; or .jpg, 2 MB max)
```

`<mod id>` must be your `manifest.json`'s `id`. `<Author>` is your name with
`@`, `/` and `\` removed. Copy [`examples/YourName@example_mod/`](examples/YourName@example_mod)
and edit it, then check your work:

```sh
node scripts/validate.mjs mods/YourName@your_mod
```

## Before you submit

- `python3 tools/modkit.py validate your_mod --strict` passes in the engine repo.
- `python3 tools/modkit.py lint your_mod` passes — **no ROM-derived content**
  in anything you distribute. No extracted PNGs, no chip-audio banks, no ROM
  images, no IPS/BPS/UPS patches. Derived art ships as an asset transform.
- Your download is a `.zip` with the mod's files **at the archive root**, not
  nested in a folder. `python3 tools/modkit.py add-release-workflow your_mod`
  produces exactly that.
- `meta.json` matches your `manifest.json` — same `id`, `api`, `profile`,
  `permissions`, `dependencies`, `conflicts`.

## Keeping the listing current

If your entry has `"github": "owner/repo"` and leaves `automatic_version_check`
on, **do not open a pull request to bump a version**. Tag a release in your own
repo; the nightly job picks it up.

Open a PR to change the listing itself: description, categories, tags,
thumbnail, a moved repository, or a mod that is no longer maintained (say so in
the description — a listing that quietly rots helps nobody).

## What the sandbox scan looks for

CI reads the Lua inside your release zip and checks it against the engine's own
sandbox policy (`src/mods/Sandbox.lua`). These fail the run outright, because
the sandbox refuses them at runtime and a mod built on them cannot work:

- `require` of `io`, `os`, `debug`, `package` or `ffi`
- `require` of a `love.*`, `ffi.*` or `jit.*` submodule
- `require` of `socket`, `enet`, `http`, `https`, `ssl`, `mime` or `ltn12`
  without `"network"` in your permissions

These do not fail anything, but they are printed for a human to read: a
computed `require`, `load`, `loadstring`, `dofile`, `string.dump`, `getfenv`,
`setfenv`, and indexing `_G` with a computed key. All have honest uses; a scan
just cannot see through them.

Files under `tests/`, `spec/` or `workers/`, and anything ending `_test.lua`,
`_spec.lua` or `_worker.lua`, are reported rather than blocking — a love.thread
worker runs in its own Lua state and a test runs on your machine, so neither
passes through the sandbox. The contents of `[[ long strings ]]` are skipped
for the same reason: that is how worker source travels.

The scan runs on your pull request **and again every time the index picks up a
new release of your mod**. A version that does not pass is held: the index goes
on serving the last release that did, and an issue is opened here. Merging is
not a permanent pass.

## When a listing goes dead

A job runs every six hours and probes every entry: the `github` repo has to
resolve, and a `downloadURL` has to answer with something that is not a 404
and not an HTML page.

An entry that fails takes a strike. Four consecutive strikes — a full day of
staying broken — and the folder is deleted and the removal is recorded in an
issue. One passing probe clears the count, so a repo that blips is never at
risk.

Ceilings sit above that. If entries break in a batch, if too many probes come
back inconclusive, or if more than five entries are due for removal at once,
the whole run is skipped: nothing recorded, nothing removed, nothing committed.
A wave of failures is a GitHub outage far more often than it is a wave of
authors deleting repos on the same afternoon.

If your entry was removed, fix the repo or the link and open a fresh
submission. Nothing is held against you, and the git history still has it.

`blocklist.json` is the exception: a name listed there fails CI on sight.
It is a maintainer decision, not an automatic one, and each entry records
why and when.

## What review looks at

CI checks shape, naming, and that the download resolves. A maintainer then
checks the parts a machine cannot:

- the metadata describes the mod that is actually there
- the archive installs the way the launcher expects
- declared permissions match what the code does
- nothing distributed is ROM-derived
- the mod is presented as its author's own work, not as an official product

## House rules

- One entry per mod. Reuploads of someone else's work get closed — link to the
  original instead.
- Name and present your mod as yours. No official branding.
- Descriptions are rendered as markdown with HTML stripped. Do not bother with
  script tags.
- A listing is not an endorsement, and the index makes no claim that a mod is
  safe to run.
