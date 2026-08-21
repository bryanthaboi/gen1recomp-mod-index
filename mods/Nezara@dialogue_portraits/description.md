# Dialogue Portraits

A face beside the words, the way Stardew does it. Talk to someone and their
portrait appears next to the dialogue box.

## What it changes

- **Every trainer class gets a portrait automatically.** All 45 classes have
  a hand-edited bust, cropped from the ROM's own battle art and tinted with
  BROWNMON, a real palette from the game's own data. A trainer's pre- and
  post-battle speech both get one too — only text drawn during the battle
  itself doesn't.
- **28 talking Pokémon NPCs get one too** — every species with a talking
  overworld line (the Fan Club's Pikachu, Mr. Fuji's Psyduck, both Snorlax
  blocking a route, ...), hand-drawn and mirrored to face the text on
  whichever side it lands.
- **Three layouts**: INSET draws the art inside the dialogue box in its own
  columns; FRAMED gives it a separate bordered Game Boy panel; MARGIN paints
  it in the letterbox and leaves the box untouched. `SIDE = AUTO` puts the
  face on whichever side of the screen the player turned toward.
- **Speaker detection isn't a guess where the game can be asked directly.**
  It reads the dialogue's own "NAME: " prefix first when the ROM's text has
  one, then the running script's own NPC, then the player's facing cell —
  so scripted encounters and mid-script speaker handoffs (Oak's Lab: Oak
  talks, then the rival cuts in, same script) are covered, not just plain
  talk to an NPC standing still.
- **Custom art for everyone else.** Drop a PNG in `CustomArt/` named after a
  trainer class or overworld sprite (or a story character's name) and it
  overrides the built-in art, no code required. The mod's own README ships
  two reference tables — every trainer class's overworld sprite, and every
  other NPC sprite's current portrait coverage — so it's easy to see what
  still needs art.

## Install

1. Download `dialogue_portraits-1.0.2.zip` from the [releases page](https://github.com/Nezara/gen1recomp-dialogue-portraits/releases).
2. In the launcher, MODS → **Import mod .zip**.
3. Enable it and start (or continue) a game — no save migration involved.

With `github` set in the manifest, the launcher's **Update** and **Versions**
buttons take over from here.

## Compatibility

- Mod API 2, engine `>=0.0.0-0 <2.0.0`.
- Pure `content` profile: link play is unaffected.
- No known conflicts, though anything else that also narrows or wraps
  `TextBox` is worth testing alongside it.

## Credits

Idea originally proposed by Grxpe Ape #TEAMKRIS (Boi's Club Games Discord);
implementation by Nezara. The portrait art is derived from the Pokémon Red
ROM (cropped and recolored battle sprites, hand-edited on top) — see the
mod's own README for the "Assets and licensing" section covering that.
