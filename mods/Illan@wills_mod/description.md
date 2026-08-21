# Encounters Guide

A map-first wild-encounter guide for Gen1Recomp: the real Kanto Town Map is
the menu. Walk it, hop between encounter-bearing locations, and drill down
to exact routes, floors, caves, and buildings — with truthful level ranges
and per-step odds derived from *your* imported ROM.

## What you get

- **Map-first navigation** — START → PKMN MAP drops you on the imported
  ROM's own Town Map. D-pad between glowing markers, press A, and you're
  inside that location's exact encounter tables.
- **Exact source identity** — floors, caves, gates, buildings, and Pokémon
  Centers are never blended: `-- MT. MOON 1F`, `-- MT. MOON B1F`, and
  `-- MT. MOON B2F` stay separate, never-merged sources.
- **Truthful data** — LAND and WATER/SURF are separate views; level ranges
  are compact (`ZUBAT Lv. 8-10`), and every exact level shows its chance
  per movement step.
- **You are here** — a blinking white marker shows your current location,
  even where that spot has no wild encounters.
- **Walking HUD** — while exploring, a panel lists the current area's LAND
  and WATER species with level ranges; AUTO (grass/water only), ALWAYS, or
  OFF, with SMALL/MEDIUM/LARGE sizes, from the Options menu or the **H** key.
- **Complete list** — SELECT opens every encounter source, including any
  that lack Town Map coordinates.

## Install

1. Open **MODS** in Gen1Recomp (`F10` on desktop).
2. **Import mod .zip** and select `wills_mod-1.0.1.zip` from the
   [releases](https://github.com/illanrego/wills-mod/releases).
3. Enable **Encounters Guide**.

Works on desktop and Android. Requires an imported Pokémon Red, Blue, or
Yellow ROM. Updates come through the in-game mod manager via the mod's
GitHub repo (`github: illanrego/wills-mod`).

## Notes

- Read-only: never touches saves, encounter mechanics, or link state
  (`affects_link: false`), no permissions, API 2.
- No ROM-derived bytes are shipped — everything is derived at runtime from
  the player's own import.
- MIT licensed; source: https://github.com/illanrego/wills-mod
