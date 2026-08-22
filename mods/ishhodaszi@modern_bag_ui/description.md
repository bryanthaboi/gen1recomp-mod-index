# Modern Bag UI

Modern Bag UI rebuilds the bare item list as a responsive, pocket-based Bag while keeping Gen 1's font, palettes, sounds, and item behaviour.

Alongside an **All** list in acquisition order, five pockets organise Items, Medicine, Poké Balls, TMs/HMs, and Key Items. Left and right switch pockets, each pocket remembers its cursor, and items can be safely reordered. The same design carries into the PC's Withdraw, Deposit, and Toss screens.

Two skins are included: a colourful modern layout and a classic Pocket-style layout. Both adapt across compact 160×144 play, widescreen windows, and portrait phones, with readable details, quantities, money, and capacity. Item descriptions remain translatable through the engine's string catalogue.

Gen1Recomp save files can hold up to 255 unique Bag and PC stacks with quantities up to x999. Exporting back to an original cartridge `.sav` still uses the hardware-era 20/50-stack and x99 limits, so overflow should be moved or reduced before export.

Item use, party targeting, battle turns, TMs/HMs, fishing, bicycles, and scripted Bags continue to use the engine's built-in controller. The mod requires `engine_internals` to retain that behaviour while replacing the presentation and extending storage.
