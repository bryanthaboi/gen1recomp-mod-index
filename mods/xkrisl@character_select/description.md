## What it does

Choosing a character changes:

Overworld, battle, trainer card, hall of fame.

## Character roster

Dir.
```text
mods/
└── character_select/
    ├── characters.lua    <-- edit this to control the menu
```

Adjusting individual characters.
```lua
return {
    { label = "DEFAULT PLAYER", vanilla = true },
    { label = "BROCK", overworld = "SPRITE_SUPER_NERD", trainer = "OPP_BROCK" },
    { label = "MISTY", overworld = "SPRITE_BRUNETTE_GIRL", trainer = "OPP_MISTY" },
    { label = "LANCE", overworld = "SPRITE_LANCE", trainer = "OPP_LANCE" },
}
```
You can adjust the in-game text, overworld sprite, and the trainer card sprite. Mix and match if you'd like!

## Notes

- This has only been tested on Pokemon Yellow.
- This has only been tested on gen1recomp v0.1.77.
