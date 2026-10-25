# Move Damage Info

While you pick a move in battle, the TYPE/PP box shows the damage that move
would deal right now, with two more pages for its numbers and a
plain-language description of what it does.

## What it changes

- **Page 1 (default)** in the move-select box: `DMG 12-14` against the foe in
  front of you, the move's type and its PP.
- **Page 2** (Left/Right switches pages): `PWR 95`, `ACC 100` and the type
  multiplier (`X1/4` … `X4`).
- **Page 3**: a short description of the effect, e.g. `LOWERS / ATTACK` for
  Growl or `MAY / BURN` for Ember.
- **SELECT** opens a text box with the same information in words: the effect,
  power, accuracy, the damage range, the percentage of the foe's HP, the
  matchup and the PP.
- The mod's own text is available in English, Italian, Spanish and Portuguese
  (`MODS → Move Damage Info → LANGUAGE`, or the `MOVE INFO LANG` row in
  `OPTION`). Move and type names stay the cart's, so they follow the game and
  any translation mod.

The damage is not an estimate: it calls the cart's own calculator
(`src.battle.Damage.compute`) twice, with the lowest and the highest random
roll and without a critical hit, so stats, stat stages, badge boosts, burn,
Reflect/Light Screen, STAB, the type chart and the 217–255 random factor are
all accounted for. Multi-hit moves report the damage per hit.

## Install

1. Download `move_damage_info-1.2.0.zip` from the releases page.
2. In the launcher, MODS → **Import mod .zip**.
3. It is on by default; turn it off from `MODS → Move Damage Info` or from the
   `OPTION` menu.

## Compatibility

- Mod API 2, Gen 1 only (Red, Blue and Yellow).
- Pure `content` profile: link play is unaffected.
- Works with the classic and the wide battle layout.
- Does not draw anything for a disabled move, so the cart's own `disabled!`
  message stays as it is.
- No known conflicts. It replaces the contents of the cart's TYPE/PP box, so a
  mod that also repaints that box (e.g. a move-matchup overlay) will fight it
  for the same pixels.

## Credits

Written by cchrkk. MIT licence; no ROM-derived content, the ball/box drawing is
the cart's own text rendering.
