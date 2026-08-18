# Item Randomizer

Item Randomizer creates a persistent per-save item mapping for supported sources in **Pokémon Red, Blue, Yellow, and Gold**. Its ordinary pools exclude key items, HMs, non-tossable items, and other progression-sensitive rewards.

## Features

Players can independently enable visible item balls, hidden finds, shops, berries, eligible scripted gifts, eligible existing held items, and the protected New Game PC reward. Reduced low-value weighting and progression-aware weighting keep ordinary rewards useful while retaining the possibility of an early lucky find. Shop inventories and prices remain persistent per shop after generation.

In Gen 1, **REROLL NEW GAME PC ITEM** is a one-shot action for the generated PC item: it rerolls the item, resets itself, returns to the overworld, and permanently locks only after the initialized contents have left the PC. The manual PC-item selector is Gold-only.

## Install

Download the newest `item_randomizer-<version>.zip` from the [release page](https://github.com/inmento/Item-Randomizer/releases). In Gen1Recomp, open **MODS**, choose **Import mod .zip**, import the archive, and enable the mod.

## Compatibility

The mod targets API 2 and supports Gen 1 and Gold. It uses the active game version to keep Gen 1 and Gold option paths separate, and includes safe dynamic filtering for supported Crystal 251 installations.
