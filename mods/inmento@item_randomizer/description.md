# Item Randomizer

Item Randomizer creates a persistent per-save mapping for independent item-source categories. It supports visible item balls, hidden finds, an optional New Game PC item, and progression-weighted results with a lower weight for common low-value items.

Gold adds native support for item balls, hidden pickups, berry trees, ordinary scripted gifts, eligible existing held items, and the protected New Game PC reroll. Key items, HMs, non-tossable items, and other progression-sensitive rewards stay outside ordinary pools. Berry handling leaves apricorn trees unchanged, and held-item handling never gives an item to a Pokémon that was originally itemless.

The PC reroll affects only the generated starting item and permanently locks after it is withdrawn.
