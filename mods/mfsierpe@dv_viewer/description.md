# DV Viewer

See every Pokémon's hidden DVs and Stat Exp on a third STATS page, graded
GREAT / GOOD / OK / POOR, and opened the moment you catch something, so you
can tell at a glance whether a catch is worth keeping.

## What it changes

- **Right after a catch:** once the catch text and the nickname question are
  done, the new Pokémon's DV page opens (party or PC box). One press of A
  closes it and the battle ends as usual.
- **STATS screen, page 3:** A or B on the moves page now opens the DV page
  instead of closing; A again closes it. Works from the party menu and the PC.
- **On the page:** the DV (0–15) for HP, Attack, Defense, Speed and Special,
  with HP built from the other four the way Gen 1 does it; each Stat Exp
  value (0–65,535); a ★ on any perfect 15; and the DV total out of 60
  (Attack + Defense + Speed + Special) with a grade:

| Total | Grade | Wild odds |
|---|---|---|
| 45–60 | GREAT | about 1 in 17 |
| 40–44 | GOOD | about 1 in 10 |
| 25–39 | OK | about half |
| 0–24 | POOR | about 1 in 4 |

It only reads: it never changes a Pokémon's DVs, Stat Exp or stats.

## Install

1. Download `dv_viewer-1.0.0.zip` from the
   [releases page](https://github.com/mfsierpe/gen1recomp-dv-viewer/releases/latest).
2. In the launcher, MODS → **Import mod .zip**.
3. Make sure DV Viewer is on, then start your game: START → POKéMON → STATS
   and press A twice.

With `github` set in the manifest, the launcher's **Update** and **Versions**
buttons take over from here.

## Compatibility

- Red, Blue and Yellow (Gen 1 only); engine `>=0.3.97`; Mod API 2.
- Needs `engine_internals`: it adds a page to the built-in STATS screen.
- `content` profile, `affects_link: false`: link play is unaffected.
- Tested alongside Shiny Pokemon, which also draws on the STATS screen. A mod
  that replaces the STATS screen outright will not show page 3.

## Credits

By mfsierpe, MIT licensed. The page follows pret/pokered's status screen
layout and Gen 1's HP DV rule.
