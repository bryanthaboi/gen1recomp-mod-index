# Party Presets

Save **18 fixed team presets** (MAIN 1–3 plus every Gen 1 type) and switch the
live party to a preset without depositing and withdrawing by hand.

Presets store **references to Pokémon you already own**. They never clone,
heal, duplicate, or delete Pokémon.

## What it changes

- Adds **TEAMS** to the Start menu (before SAVE) and **TEAM PRESETS** to
  a Pokémon Center PC (before LOG OFF).
- MAIN 1, MAIN 2, and MAIN 3 accept any species. The other categories match
  Gen 1 ROM types. Dual-types can sit on both matching type presets plus any
  MAIN team (one Pokémon, not copies).
- Activate moves existing party/PC tables transactionally. Missing
  Pokémon, Day Care, a full PC, or an empty team abort the switch and
  leave the boxes alone.
- Team slots and the owned-Pokémon picker use the same 16×16 party icons
  as the party menu, including Unique Menu Icons when that mod is enabled.

This mod does not change species stats, trainers, maps, or DVs. See
`DIFFERENCES.md` in the source repo.

## Install

1. Download `PARTY_PRESETS-1.1.0.zip` from the releases page.
2. In the launcher, MODS → **Import mod .zip**.
3. Enable **Party Presets**. Existing saves work; MAIN 1 seeds from the
   current party on first enable.

With `github` set in the manifest, the launcher's **Update** and
**Versions** buttons take over from here.

## Compatibility

- Mod API 2, engine `>=0.1.0 <2.0.0`, Pokémon Yellow.
- Pure `content` profile: link play is unaffected.
- Needs `engine_internals` (party/PC box modules).
- Unique Menu Icons is optional. No known conflicts.

## Credits

Copyright (c) 2026 Mirage. MIT.
