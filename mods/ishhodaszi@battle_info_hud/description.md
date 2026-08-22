# Battle Info HUD

Battle Info HUD adds missing battle-reading information to Gen1Recomp's existing HUD while preserving its original panels, curves, font, and tiles.

It redraws the native HP meters with clear green, yellow, and red states; extends the player panel with a slim EXP strip and progress readout; places the game's Poké Ball tile beside opponents whose species has already been caught; and gives status and level labels a cleaner shared alignment.

The presentation adapts to classic, WIDE, and supported staged voxel battle layouts. Gender Mod markers are kept aligned with the adjusted player level row, and compatible staged renderers retain ownership of their world, sprites, and HUD placement.

The mod changes presentation only. It does not alter stats, EXP gains, catches, status effects, battle rules, or ordinary save data. A **BATTLE INFO** setting in the normal Options menu restores the original minimal HUD at any time.

The package contains no ROM-derived assets. It requires `engine_internals` so it can augment Gen1Recomp's built-in battle renderer and reuse its native font and HUD tiles.
