# A box you can actually see

Gen 1's PC shows twenty names in a list, and moving a Pokemon between boxes
means withdrawing it, changing box, and depositing it again. This is the
Ruby/Sapphire answer to that.

A 5x4 grid of the current box. **A** picks a Pokemon up and **A** puts it
down, swapping with whatever is already in the slot. **B** over a Pokemon
opens its summary. **START** closes. **SELECT** crosses to your party and
back, which is how you deposit and withdraw. Walking off the left or right
edge changes box.

`OPEN FROM` chooses where it is reachable: the start menu, the Pokemon
Center PC, or both. The vanilla box PC is left in place either way.

## Why the grid uses battle pics

Gen 3's grid works because every species has its own icon. Gen 1 has no such
thing: the icon table maps a species to one of a handful of shapes and the
whole game carries four icon images, so a grid of those would be twenty
identical blobs — strictly worse than the list it replaces. The grid draws
each Pokemon's front pic at exactly half scale instead. The integer divisor
keeps two-bit pixel art crisp, and the arithmetic fits: five columns of 28
is 140 across a 160-wide screen, four rows is 112 of the 144 down.

They are read through the engine's `Assets.image`, the same seam a sprite
mod shadows, so an animated-sprite mod's art shows up in this grid too.

## Safety

A box stays a compact array — the shape the save format and the vanilla PC
read — so dropping into an empty cell appends rather than leaving a hole.
The party can never be emptied, a box never passes 20 and a party never
passes 6, and if you are carrying a Pokemon while both are full the screen
refuses to close rather than dropping it out of the save.

## Wallpapers: sixteen places, ninety-one of them

Every box wears a scene, and **no scene has fewer than five wallpapers behind
it**. SEA, FOREST, SKY, CAVE, CITY, SNOW, NIGHT, DESERT, VOLCANO, SPACE,
CASTLE, SAKURA, STORM, CIRCUIT, TRAIN and 90S are each drawn in code -- that
is the `GEN3 BOX` entry, the one a box wears until you change it -- then
drawn again by pixel artists whose work is CC0 or CC BY, and then again
through other palettes: `SAKURA < GEN3 NIGHT >` is a night hanami, not a
toggle.

Twenty-seven outside hands are credited in `THIRD_PARTY_NOTICES.md` and, more
usefully, **in the menu itself**: the artist's name is the label you scroll
through. Up and down change the place, left and right change the hand, and
the box behind the menu wears whatever the cursor is on -- the menu *is* the
preview. `SELECT` keeps one as a favourite, and the FAVOURITE scene wears
what you kept. Each box remembers its own pair.

Whether a layer moves is measured rather than guessed: the mean difference
between its first and last column says whether it continues into itself, so
clouds and water drift while buildings and rock hold still. A still layer is
not a dead one -- it pans slowly across whatever width it has spare and turns
back before the join could show.

**The list is open.** One pull request, one wallpaper, and the artist's name
becomes the label players scroll through -- see CONTEST.md in the repository.
A check on the pull request measures every layer and tells you which of them
the box will let move.

`SLOTS` sets how opaque each cell is over the scene, `BANDS` how much of the
title row and the footer the scene gets, and `ANIMATE` turns the drift off
for anyone who would rather it held still.

Lua source only: no ROM, no ROM-derived data, no game assets.

**On Gold.** Runs on Pokemon Gold as well as Red, Blue and Yellow: fourteen boxes of twenty instead of twelve, Gold's own summary screen, its split Special in a withdrawn Pokemon's stat block, and its MAIL rules honoured (a Pokemon holding mail cannot be boxed, exactly as the vanilla PC refuses it). GRID BIG is Gen 1 only -- Gold's boot scales a single Game Boy canvas and never asks a screen how big it would like to be.

**On Ruby, Sapphire and Emerald** (since 1.27). Gen 3 already has a box screen, so the mod keeps the cart's own PC and builds on it. With FULL SCREEN on (the default, as on Gen 1 and 2) the PC opens straight into **ALL BOXES**: every box on one screen, laid out for a phone held upright or for a desktop, with a PKMN DATA card that plays the Pokemon's own Emerald animation, the party as a row over the boxes, Pokemon moved by finger drag or tap through the game's own rules, each box's menu from its name, and zoom by wheel or pinch down to one box with each Pokemon's front picture. Around it: eighteen more wallpapers sorted into themes next to the game's own, previewed on the box as you scroll; fifteen skins and twenty pointers; touch and the mouse wheel; BOX HEALS; a BOXES row on the START menu. Every one of these has its own switch in the mod's options, under the same names as on Gen 1 and 2. Verified in game on Emerald; Ruby, Sapphire, FireRed and LeafGreen are untested.
