# Exp Multiplier

An **OPTIONS** EXP multiplier for Pokémon Yellow. Cycle LEFT/RIGHT:

**OFF → 1.5X → 2X → 3X → SCALED → OFF**

OFF is vanilla EXP. The other modes multiply the battle EXP number after
the engine (and Exp Share, if present) have already computed the share.
The printed `"X gained N EXP. Points!"` line shows the multiplied amount.

## What it changes

- Adds **EXP MULTIPLIER** to OPTIONS (and the matching choice in the
  MODS manager). The setting is per save and defaults to OFF.
- Multiplies only `mon.exp`. Stat exp, DVs, growth rates, and the level
  cap are unchanged. Day Care step-exp stays vanilla.
- **SCALED** is a moderate, level-based boost so late-game leveling is
  less tedious without melting early gyms:
  `factor(level) = 1.25 + 1.75 * (level / 70) ^ 1.5`, clamped to
  `[1.25, 3.0]`. It uses the receiving Pokémon's level.

This mod does not change species stats, trainers, maps, or DVs. See
`DIFFERENCES.md` in the source repo.

## Install

1. Download `EXP_MULTIPLIER-1.0.0.zip` from the releases page.
2. In the launcher, MODS → **Import mod .zip**.
3. Enable **Exp Multiplier**. Existing saves work; the row starts at OFF.

With `github` set in the manifest, the launcher's **Update** and
**Versions** buttons take over from here.

## Compatibility

- Mod API 2, engine `>=0.1.0 <2.0.0`, Pokémon Yellow.
- Pure `content` profile. Multiplied EXP can desync versus a partner
  without the mod; `affects_link` stays false.
- Needs `engine_internals` (`exp.gain`).
- **Exp Share** (`exp_share`) is optional. Exp Share decides who gets a
  share and the split; this mod scales how much that share is. OFF on
  either side leaves the other unchanged. No known conflicts.

## Credits

Copyright (c) 2026 Mirage. MIT.
