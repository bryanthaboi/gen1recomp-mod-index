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

Lua source only: no ROM, no ROM-derived data, no game assets.

**On Gold.** Runs on Pokemon Gold as well as Red, Blue and Yellow: fourteen boxes of twenty instead of twelve, Gold's own summary screen, its split Special in a withdrawn Pokemon's stat block, and its MAIL rules honoured (a Pokemon holding mail cannot be boxed, exactly as the vanilla PC refuses it). GRID BIG is Gen 1 only -- Gold's boot scales a single Game Boy canvas and never asks a screen how big it would like to be.
