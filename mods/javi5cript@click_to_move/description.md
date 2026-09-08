# Mouse Adventure

Play Pokémon Red, Blue and Yellow with the mouse. Hold the left button to walk,
point to steer in eight directions like a Diablo-style click-to-move, and click
the things around you — NPCs, signs, items, dialogue boxes and menus — instead of
reaching for the keyboard. Native battles, collision and saves are untouched.

## What it changes

- **Point-to-steer overworld movement.** Hold left-click and Ash walks toward the
  cursor; the direction resolves to the eight-way grid the engine already uses.
- **Click to interact.** Click an adjacent NPC, sign, or item to talk, read, or
  pick it up. Click dialogue to advance it, and click menu entries to choose them.
- **Right-click to go back.** Acts as the B button for cancelling and closing menus.
- **On-screen action dock.** A small always-available control strip for players who
  want every input on the mouse, including the start menu.

## Install

1. Download `click_to_move-1.2.0.zip` from the
   [releases page](https://github.com/javi5cript/gen1recomp-mouse-adventure/releases).
2. In the launcher, **MODS → Import mod .zip**.
3. Enable it and start (or load) any Red, Blue, or Yellow game.

With `github` set, the launcher's **Update** and **Versions** buttons take over from here.

## Compatibility

- Mod API 2, engine `>=0.2.56`.
- Pure `content` profile: link play is unaffected.
- **Turn off voxel/tilt rendering** for held steering — the tilted camera changes how
  cursor direction maps to the grid.
- Most built-in screens are clickable, but a few third-party **replacement UIs** aren't
  wired for mouse targeting yet; the keyboard still works everywhere as a fallback.

## Status

Public beta. Core loop — movement, dialogue, menus, naming, battles and saves — is
covered on Red/Blue/Yellow. Please report any screen that doesn't take clicks.

## Credits

Built by javi5cript. Released under the MIT license. Ships no ROM-derived content.
