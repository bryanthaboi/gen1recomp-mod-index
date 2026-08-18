# Sound Effect Replacer

Sound Effect Replacer lets players replace selected audio in **Pokémon Red, Blue, Yellow, and Gold** through a simple two-folder layout: **General Sound Effects** for common categories and **Specific Sound Effects** for exact control.

## Features

The mod exposes every current named engine sound-effect label, optional move sounds for all 251 move IDs, evolution in-progress and completion audio, species cries, and all 42 special Yellow Pikachu voice clips. A single shared folder works for a cue in whichever supported game is currently running.

Replacement files can use the formats decoded by the bundled LÖVE runtime, including WAV, MP3, FLAC, Ogg Vorbis, and supported tracker/module formats. Ogg Opus is detected and skipped with a diagnostic warning because it is not supported by the runtime.

The optional PotatoVoxel integration uses an original Lua-authored chip confirmation cue only when that mod is enabled; it remains silent otherwise.

## Install

Download the newest `sound_effect_replacer-<version>.zip` from the [release page](https://github.com/inmento/Sound-Effect-Replacer/releases). In Gen1Recomp, open **MODS**, choose **Import mod .zip**, import the archive, and enable the mod.

## Compatibility

Sound Effect Replacer targets API 2 and supports Gen 1 and Gold. Replacement audio is configured per player by placing one supported file in the desired existing target folder and restarting Gen1Recomp.
