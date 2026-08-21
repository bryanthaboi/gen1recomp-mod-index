# Battle Cinematics - Dynamic 3D Battle Camera

**Battle Cinematics (BC)** is a modular battle camera director for Pokémon Gen1Recomp, with current support across **Gen 1 and Gold / Gen 2**.

It adds authored cinematic camera systems while leaving Pokémon models, sprites, battle stages and effects in the hands of the active presentation backend.

> **Stadium supplied the cinematography. BC supplied the camera system.**
>
> **Stadium models are not required.**

## What it adds

- **Stadium 64** — a source derived recreation of Pokémon Stadium's passive battle camera language, adapted to Recomp arenas and BC's shared safety systems.
- **DW3 Classic** — orbital, over the shoulder and environmental battle framing inspired by Digimon World 3.
- **Hero Portrait** — calmer close three quarter Pokémon presentation with less physical travel.
- **PKMN Intro Cam** — cinematic FULL / COMPACT send in presentation for Pokémon entering battle.
- **Attack Camera** — Stadium inspired, move aware attack cinematography.
- **Faint Camera** — dedicated final composition for defeated Pokémon.
- **Manual camera** — BC owned right stick control on Gen 1, with provider aware interoperability on supported Gold hosts.
- **Idle Preset configuration** — Framing, Orbit Speed, Height and Angle controls for Stadium 64, DW3 Classic and Hero Portrait.
- **Idle View** — Standard / Wide / Extra Wide / Ultra Wide optical views for BC authored idle cameras.
- **Shared camera safety** — map boundary, wall traversal, renderer dead zone and battle floor protection for BC owned shots.

## Presentation philosophy

Battle Cinematics is renderer independent by design. It attaches to compatible live battle camera and presentation seams instead of replacing another mod's renderer or model set.

> **BC respects what the underlying system provides, then makes the best cinematic use of it.**

> **Every BC option produces a good, readable battle everywhere, with BC free to gracefully degrade its physical camera language when the environment cannot support it.**

## Compatibility

Current validated presentation environments include:

- Dramatic Shape
- Dramaless Shape
- PotatoVoxel
- Voxel Ascendant
- Battle Art Voxel Fork
- StadiumBattleFX
- Gen2-3D-Sprites / `STADIUM2_OVERWORLD_MODELS`
- Pokémon Stadium 2 Importer / `STADIUM2_IMPORTER`

`EXTERNAL` is a permanent Idle Preset that yields passive / idle camera ownership to the active presentation host while BC's other enabled cinematic phases remain independent.

### Gen 1 + Gold

BC supports both **Gen 1** and **Gold / Gen 2** presentation paths. Gold integrations preserve provider owned right stick behaviour rather than globally reusing the separate Gen 1 manual camera subsystem.

Stadium2 Importer support has been validated with its live Stadium2 presentation on both generations, while the existing Randy / Gen2-3D-Sprites path remains independently supported.

## v1.0.10

- Loads safely and remains inactive when no compatible battle presentation backend is enabled, instead of failing the mod load.
- This is a loader and index compatibility hotfix only; supported backend camera behaviour remains unchanged from v1.0.9.

## v1.0.9 feature highlights

- Expanded Stadium 64 and Hero Portrait preset configuration.
- Added the wider Extra Wide / Wide / Standard / Near / Close framing ladder across configurable Idle Presets.
- Added independent Idle View control.
- Added shared battle floor protection for BC owned cameras.
- Hardened Gen 1 manual right stick takeover against stale transition input and unintended continuous orbit.
- Reorganised the options menu around Idle Preset and Pokémon Intro camera systems.
- Preserved all established v1.0.8 Gen 1 + Gold backend and provider compatibility.
- No forced settings migration.

## Install

1. Download the latest `BATTLE_CINEMATICS-<version>.zip` from the GitHub Releases page.
2. In Gen1Recomp, open **MODS → Import mod .zip**.
3. Enable **Battle Cinematics - Dynamic 3D Battle Camera**.
4. Enter a battle and configure the camera from the mod's options page.

Battle Cinematics uses the `content` profile and declares `engine_internals`. It does not affect the link fingerprint.

## Source and releases

Source, documentation, media and installable releases are maintained at:

`EnterPlayerOne/Battle-Cinematics-Stadium-Camera`

## Credits

Battle Cinematics is developed by **EnterPlayerOne**.

Scoped external acknowledgements and compatibility credits are maintained in the project README. External renderers, Pokémon models, sprites, effects and provider cameras remain the work of their respective authors.
