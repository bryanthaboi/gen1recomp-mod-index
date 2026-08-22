# Typed Move Colors

Typed Move Colors can turn each move into a chamfered type-coloured card or leave the native interface intact and colour only its move-name text. Both presentations retain Pokémon Red, Blue, and Yellow's original font and read the live merged move registry, so renamed moves, balance changes, and custom types are respected.

Colours appear in battle move selection, Pokémon summaries, move forgetting, Mimic, and PP-item targeting. Responsive battle cards include full type, Power, PP, and optional effectiveness indicators. They adapt to classic, WIDE, high-DPI, short landscape, and portrait-safe layouts without replacing the battlefield, sprites, or status HUD.

Text Only mode restores the active renderer's original boxes, cursor, PP panel, and controls, then adds brighter move-name and selected-type ink. Settings also control battle and menu coverage, wide or game layout, effectiveness hints, soft/bold/vibrant palettes, and card opacity.

Compatibility paths preserve the presentations supplied by popular modern UI and staged battle mods while adding type information where they expose suitable hooks. Unknown custom types use a neutral fallback.

The mod changes presentation only and requires `engine_internals` to augment Gen1Recomp's existing battle and menu drawing without replacing move behaviour.
