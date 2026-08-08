# Dramatic Sky Ride

Dramatic Sky Ride adds controllable Pokémon mounts to Gen1Recomp, with dedicated systems for flying, terrestrial riding and visible Surf mounts. The current stable release integrates with Battle Art Voxel Fork and PokéPC overworld sprites while preserving native map interactions, encounters and field logic.

## Features

- Flying mounts including Charizard, Pidgeot, Fearow, Golbat, Aerodactyl, Articuno, Zapdos, Moltres, Dragonair and Dragonite.
- Ground Ride mounts including Arcanine, Rapidash, Dodrio, Rhyhorn, Rhydon, Kangaskhan, Tauros and Snorlax.
- Visible Surf mounts for Blastoise, Tentacruel, Gyarados and Lapras.
- Species-aware acceleration, speed, gallop strength, stamina and rider positioning.
- Pokédex-proportional mount sizing with per-species size controls.
- Story-aware progression and discovery gates for mount access.
- Safe battle and connected-map restoration for mounted states.
- Native NPC, sign, collision, encounter and field-action behavior retained wherever possible.
- Wild Skies integration with aerial interceptions; version 1.4.1 or newer is strongly recommended.
- Surf-specific Battle Art 3RD camera compatibility keeps the trainer and Surf mount visible over water.
- Keyboard and controller shortcuts for ground riding and flight.

## Requirements

- Gen1Recomp with Mod API 2 support, compatible with `>=0.1.69 <2.0.0`.
- Battle Art Voxel Fork `>=1.7.6 <2.0.0`.
- `PokePCFollowers_VoxelMerge` for the required overworld Pokémon sprites.
- Wild Skies `>=1.4.1 <2.0.0` is optional but strongly recommended.

Dramatic Sky Ride conflicts with `free_fly`.

## Controls

- Ground Ride: `G` or `SELECT + L1`.
- Flight / takeoff: `H` or `SELECT + R1`.
- Boost / gallop: the configured in-game `B` action.
- Ascend / descend in flight: `Page Up` / `Page Down` or `R2` / `L2`.

## Updates

The Mod Index entry tracks `mfrtechconsult/dramatic-sky-ride` with `automatic_version_check` enabled. Future stable GitHub Releases are therefore picked up by the index's nightly refresh without requiring a dedicated version-bump pull request.
