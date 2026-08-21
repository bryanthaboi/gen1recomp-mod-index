The Pokédex as a **grid of pictures** instead of a list of names.

The engine's own dex list describes itself accurately: a dex-ordered list of
151 text rows with seen/owned markers. This replaces that list with a 5×4
grid of battle pictures, and shows three states at a glance — species you
**own** are drawn in their own colours, ones you have **seen but not
caught** are dimmed, and ones you have never met are blanks.

**Colour.** A palette zone binds a palette to a tile rectangle, and the
engine draws each one scissored through its shade-remap shader, so the
number of them is a loop rather than a hardware limit: the Game Boy could
show four palettes at once, and this shows twenty-one.

**Filters.** SELECT cycles ALL / OWNED / MISSING / SEEN ONLY. MISSING is
the fastest answer to what you are still short of.

**It does not replace the species page.** Pressing A opens the engine's own
`DexEntryMenu`, so a mod that adds pages there — Useful Dex, for instance —
keeps working, and its pages are one press further in. The two stack rather
than conflict.

**GRID BIG** asks the renderer for a 320×288 surface, which is what lets a
56×56 battle picture draw at scale 1 rather than halved. GRID CLASSIC keeps
the Game Boy screen, in greyscale: a 28-pixel cell is three and a half
tiles and a palette zone must be tile-aligned.

**What it does not do:** it does not make the Pokémon sharper — the
pictures are the game's own art and cannot be redrawn, so the larger
surface buys room and colour, never detail. It reads the save's dex and
writes nothing.

Lua source only: no ROM, no ROM-derived data and no game assets.

**On Gold.** The dex covers Johto rather than stopping at Mew, the caught half is read where Gold actually keeps it, and DATA and AREA open Gold's own dex entry. GRID BIG works there too, through the widescreen contract Gold's own screens use -- only the per-species palette zones stay Gen 1, because Gold colours itself.
