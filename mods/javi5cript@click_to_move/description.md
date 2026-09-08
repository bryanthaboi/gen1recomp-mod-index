# Mouse Adventure

**Hold to move, point to steer. Click to interact.**

Play Pokemon Red, Blue and Yellow with mouse-first controls. Hold left-click
and point to steer in eight directions, click nearby characters and objects,
and navigate supported dialogue, menus and battles. This is not
click-to-destination or pathfinding. Native battle rules, progression,
collision and saving are preserved.

Designed for a clean Gen1Recomp installation with Mouse Adventure enabled.
No other mods are required.

## What it changes

- **Held steering in flat and engine TILT views.** Release to stop after
  the current tile step. Click directly on a following Pokemon to talk;
  holding past it steers instead.
- **Clickable screens.** Native dialogue, battle choices, party
  SWITCH / STATS / CANCEL menus, summary pages, Pokedex DATA / CRY / AREA
  menus, area maps and trainer cards.
- **Wheel navigation.** Scroll supported lists, Pokedex notes and moves, or
  change supported entry tabs without confirming. Enabled by default;
  overworld wheel zoom is unchanged.
- **Readable action dock.** DPI-aware text, three sizes, small-window pages,
  contextual help and Game Boy controls. Right-click goes back or cancels.
- **Guide controls and optional precision.** Toggle the guide with G
  (H/J selectable) or the dock. Early-click buffering, click-versus-hold
  separation and projected player anchoring are opt-in.
- **Aligned click targets.** Zoomed-out menus, anchored save confirmations
  and classic overlays in wide battles use the displayed UI geometry.

## Install

1. Save your progress and close the game.
2. Download `click_to_move-1.4.0.zip` from the
   [v1.4.0 public-beta release](https://github.com/javi5cript/gen1recomp-mouse-adventure/releases/tag/v1.4.0).
3. In the launcher, use **MODS -> Import mod .zip** and select the ZIP.
4. Enable **Mouse Adventure** for Red, Blue or Yellow, then start the game.

Use the release asset, not GitHub's automatic source-code archives. The seven
mod files are at the ZIP root, without a wrapper folder. Automatic GitHub
release tracking remains enabled for this listing.

## Requirements and scope

- Requires mod API 2, **Gen1Recomp >=0.2.56 and <2.0.0**, and your own
  legally obtained Red, Blue or Yellow game data. Intended for single-player.
- The native game UI is the baseline. Use the dock's arrows and A/B controls
  when direct clicking is unavailable. Badge icons remain display-only.
- Projected player anchoring is optional and experimental.
- Optional integrations are available, but compatibility with other mods
  is not guaranteed. They are not required for the core controls.
- Keyboard/controller input takes priority. Animations, cries and scripted
  waits still apply; clicks do not bypass native gameplay restrictions.

## Status

**v1.4.0 public beta.** Full playthrough coverage across Red, Blue and Yellow
is not yet complete.

See the [README](https://github.com/javi5cript/gen1recomp-mouse-adventure#readme)
for controls and options. Report problems on the
[issue tracker](https://github.com/javi5cript/gen1recomp-mouse-adventure/issues)
with your game, versions, active mods, camera mode and reproduction steps.

## Credits

Built by javi5cript. Released under the MIT license. No ROMs, game assets,
saves, engine files or other mods are included. Unofficial fan project;
not affiliated with Nintendo, Creatures or Game Freak.
