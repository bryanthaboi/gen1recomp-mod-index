# Crystal Animated Sprites

Crystal's animated sprites in Pokemon Red, Blue and Yellow, decoded from your
own Pokemon Crystal ROM.

**No artwork is included.** The mod reads the sprites, animation frames and
timing straight out of a Crystal ROM that you supply, builds them once, and
keeps the result in the mod's own cache. Nothing from the ROM is part of the
download.

## What you get

- The enemy's front sprite plays Crystal's own animation in battle, for the
  151 Kanto species. The frames, the order and the timing come from the game's
  animation scripts.
- Crystal's picture also replaces the front sprite on the status screen, the
  Pokedex, the evolution screen, the Hall of Fame, the title screen, Prof.
  Oak's intro, trades and the credits. The Pokedex entry, the status screen and
  the side panel of Bill's PC Plus play the animation; the other screens show
  the resting frame.
- Crystal's small party icons in the party menu and the PC boxes, with their two
  animation frames.
- Transparent sprite backgrounds, so it works with mods that replace the battle
  background.

## Options

- `SPRITE COLORS`: `CRYSTAL` (default) draws each Pokemon in Crystal's colours,
  which needs the game's COLORS setting on ADVANCED. `GAME` keeps the colours of
  the game you are playing.
- `PARTY ICONS`: `CRYSTAL` (default) or `GAME`.
- `BACK SPRITES`: the animated front sprite, mirrored (default), so your own
  Pokemon animates too, or Crystal's own still back sprite.
- `ATTACK ANIMATION`: `ON` (default) plays a Pokemon's animation again when it
  uses a move. Crystal does not do this; `OFF` plays it only when the Pokemon
  appears.
- `DIAGNOSTICS`: off by default. Draws a few lines over the battle for bug
  reports on devices where the save folder cannot be opened.

## Installing

1. Install the mod and enable it.
2. When the launcher asks for a file, pick your own **Pokemon Crystal** ROM.
   English (UE) v1.0 and v1.1 are supported; the launcher checks it for you.
3. Play. The first launch builds the sprites in the background, which takes
   about half a minute. A Pokemon whose sprite is not built yet shows the
   normal one and switches as soon as it is ready.

## Limits

- Needs your own Crystal ROM. The built sprites take about 30 MB.
- Only front pictures are replaced outside battle. Back pictures and trainer
  pictures on other screens keep their usual art.
- Crystal's colours only show with the COLORS setting on ADVANCED.
- Cannot run alongside other sprite mods that replace the same slots, such as
  `crystal_animated_sprites_with_shiny_visuals`, `gen2_shiny_visuals`,
  `shiny_visuals` or `CRYSTAL_251`.
- Potato Voxel and Battle Art Voxel refill the small see-through gaps this mod
  clears on purpose, until their pending fixes are merged.
