# Item Randomizer

Item Randomizer creates a persistent per-save mapping for supported item sources in Gen 1 and Gold. Its ordinary pools exclude key items, HMs, non-tossable items, and other progression-sensitive rewards. The randomizer can cover visible item balls, hidden finds, shops, berries, eligible scripted gifts, eligible existing held items, and the protected New Game PC reward.

## Features

Source categories can be enabled independently. Reduced low-value weighting and progression-aware weighting keep ordinary rewards useful while retaining the possibility of an early lucky find. Version 1.0.8 adds persistent weighted shop inventories and generated prices for Gen 1 marts and standard Gold marts. Gold also adds its native berry, gift, held-item, and PC paths.

In Gen 1, **REROLL NEW GAME PC ITEM** is a one-shot action for the generated PC item: it rerolls the item, resets itself, returns to the overworld, and permanently locks only after the initialized generated contents have left the PC. The manual PC-item selector is Gold-only.

## Install

Download the newest `item_randomizer-<version>.zip` from the [release page](https://github.com/inmento/Item-Randomizer/releases). In Gen 1 Recomp, open **MODS**, choose **Import mod .zip**, import the archive, and enable the mod.

## Compatibility

The mod targets API 2 and supports Gen 1 and Gold. It uses the engine’s active game version to keep the Gen 1 and Gold option paths separate.
