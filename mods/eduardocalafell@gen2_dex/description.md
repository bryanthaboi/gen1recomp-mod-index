The complete Johto Pokedex (#152-251), added as real, catchable species — not
a sprite reskin of the original 151.

## What's in it

- **100 species**, Chikorita through Celebi, with real Gen 2 base stats,
  catch rates, growth rates, and Crystal-style battle sprites.
- **Dark and Steel types**, registered with their real Gen 2/3-era matchups —
  this engine's vanilla type chart is Gen 1-only and has neither.
- **Evolutions**, adapted to this engine's actual mechanics rather than
  faked. Some Gen 2 evolutions (friendship, trade-while-holding-an-item,
  Sun Stone) don't have an equivalent here, so they're substituted with the
  closest real mechanism the engine has — see the repo README for the full
  list and reasoning. Tyrogue's real stat-based 3-way split (Hitmonlee /
  Hitmonchan / Hitmontop) ported without any simplification needed.
- **Thematic wild placement**: new species are woven into existing Kanto
  routes by matching the vanilla encounter table's own theme (Power Plant
  gets Mareep/Elekid, Viridian Forest gets the bug line-up, Pokemon Tower
  gets Murkrow/Misdreavus, and so on) instead of a flat chance on every
  route. Toggleable.
- The three Johto starters get their own separate small wild-spawn chance,
  since they have no canon wild habitat to place them in.
- The 6 legendaries/mythical (Raikou, Entei, Suicune, Lugia, Ho-Oh, Celebi)
  are fully registered — Pokedex entry, battles, everything — but are not
  in the normal wild tables, matching how Gen 2 never hands those out on a
  random grass step either.

## Options

- **STARTER SPAWN** (OFF/RARE/COMMON/ALWAYS)
- **ROUTE GEN2 SPAWNS** (ON/OFF)
- **DEBUG: ANY PORTED** — forces every wild encounter to a random pick from
  all 100 species, for testing/browsing rather than normal play.

## Note on the sprites

Battle sprites are Pokemon Crystal rips sourced from PokeAPI/sprites (a
CC0-licensed compilation repository; the artwork itself is Nintendo / Game
Freak / Creatures IP, same footing as any Pokemon sprite fan content). Full
provenance and the build pipeline are documented in the repo README.
