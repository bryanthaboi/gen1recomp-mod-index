Thirty more entries on the game's **COLORS** row, and eight new borders for
every text box and menu.

**The palettes.** Twelve reconstruct another machine's hardware — Amiga
Workbench, the C64 boot screen, a Virtual Boy, an amber terminal, a
Spectrum, CGA — and eighteen are colour ideas the Game Boy never had:
rainbow, fuchsia, vaporwave, sunset, toxic, noir. They join the engine's own
list rather than replacing it, so the vanilla seven keep their positions and
a save pointing at SGB still lands on SGB.

**Previewing them.** Press **A** on `OPTION → COLORS` and the menu lifts off
the game: the palette's name over the running world, left and right to walk
the list, A to keep, B to put back the one you arrived with. Choosing a
colour from a menu that is covering the game is choosing it blind.

**Riding ADVANCED.** The engine's ADVANCED mode resolves a real colour per
tile and keeps eight background palettes live at once — eighteen colours on
screen where a four-shade palette has four. Rather than switching that off,
each palette's four rungs are read as a curve indexed by luminance, so
ADVANCED's variety survives inside the palette's own hue family. Settable to
TINT, FULL, or OFF for the older four-shade behaviour.

**The frames.** THIN, DOUBLE, TRIPLE, THICK, WIDE, DASH, BEADS and TRACK,
plus GAME BOY for the engine's own. A border here is six font glyphs, so
this ships its own glyph page and repoints them.

**What it does not do.** It does not add colours to a scene the Game Boy
could not draw — four shades is still four shades, these recolour the ramp.
It changes no gameplay, no data and no save contents. Disable it with one of
its palettes selected and the game falls back to SGB; you lose the palette,
never the save.

Lua source and original artwork only: no ROM, no ROM-derived data and no
game assets. The border sheet is generated from rules in the repository's
own `tools/make_frames.py`.

**On Gold.** Both halves work. The frames ride the same Font.drawBox Gold draws its boxes with, and the palettes reach Gold's own COLOR row through GbcPalette, the choke point every colour in the Gen 2 port arrives through. The boot cinema and title screen keep the cart's grey art, which is the same boundary Gold's own DMG mode sits behind.
