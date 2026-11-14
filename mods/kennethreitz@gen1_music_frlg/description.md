# Gen 1 Music for FireRed

Plays the original Red/Blue Game Boy soundtrack in gen1recomp's FireRed and LeafGreen modes. The music is synthesized live on your device by the engine's native ChipSynth from your own imported Red. No ROM, sound bank, rendered audio, or other game-derived data is distributed.

## What it changes

- Maps 48 FireRed/LeafGreen music cues to 42 Red/Blue tracks. See [TRACKS.md](https://github.com/kennethreitz/gen1-music-frlg/blob/main/TRACKS.md).
- Sevii-specific music and one-shot fanfares and jingles keep their native versions.
- Disabling the mod restores the native soundtrack. Saves and global options are untouched.

## Install

1. Import Red in the launcher. A complete Red import is required, even for LeafGreen.
2. Download `gen1_music_frlg-v0.1.0.zip` from [Releases](https://github.com/kennethreitz/gen1-music-frlg/releases) and install it with the launcher's mod installer.
3. Enable it under Launcher > FireRed (or LeafGreen) > Mods. It is experimental and off by default.

## Compatibility

- Mod API 2, gen1recomp `>=0.4.1 <0.5.0`.
- Needs the `engine_internals` permission for the native synth. No filesystem or network permission.
- Headless integration tests pass. Audible play-testing on desktop and handheld is still in progress.
- If you change the performance tier while playing, restart the game session.

## Credits

MIT license, copyright 2026 Kenneth Reitz. Original code only. Built on bryanthaboi's gen1recomp. Inspired by DarioMelo's Music1_FRLG, which goes the other direction; none of its code or audio is included. Unofficial fan project, not affiliated with Nintendo, Game Freak, or The Pokemon Company.
