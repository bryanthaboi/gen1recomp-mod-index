# Sound Effect Replacer

**Sound Effect Replacer** provides a simple drop-in audio workflow for **Pokémon Red, Blue, Yellow, and Gold** in Gen1Recomp. Players place one replacement file in either `assets/General Sound Effects/` for friendly categories or `assets/Specific Sound Effects/` for exact control. The loaded game automatically receives the appropriate Gen 1 or Gold cue; there are no player-facing generation-specific folder trees.

The complete layout covers named engine sound effects, one optional sound per move, Pokémon cries, all forty-two Pokémon Yellow Pikachu voice clips, and both evolution moments: the music while an evolution is in progress and the completion cue before the new cry.

Sound Effect Replacer 0.3.1 accepts every audio extension decoded by the LÖVE 11.5 runtime bundled with Gen1Recomp 0.2.3, including MP3, WAV, FLAC, Ogg Vorbis, and tracker/module formats such as MOD, XM, IT, S3M, and MIDI. Ogg Opus is deliberately detected and skipped with a warning because the current runtime does not decode it.

Download the latest `sound_effect_replacer-<version>.zip` from the [release page](https://github.com/inmento/Sound-Effect-Replacer/releases). In Gen1Recomp, open **MODS**, choose **Import mod .zip**, import the archive, and enable the mod.

The simple asset-folder workflow was inspired by [Easy Custom Music](https://github.com/ty-mcdk/easy-custom-music) by **ty-mcdk**, who explicitly permitted using its code as a base. This project is **AI assisted**, not AI created.
