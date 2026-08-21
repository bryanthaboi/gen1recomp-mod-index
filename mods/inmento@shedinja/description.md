# Shedinja

**Shedinja** is a standalone Gen1Recomp species expansion for **Pokémon Red, Blue, Yellow, and Gold**. It adds Bug/Ghost Shedinja as **National Dex #292** with base HP 1, cross-generation Wonder Guard behavior, native wild encounters, a Gold rift reward path, and game-appropriate credited battle art.

| Game | Internal slot | Included art and behavior |
|---|---:|---|
| Red / Blue / Yellow | 152 standalone; 252 with Crystal 251 | Transparent Gen 1-style front/back sprites, unused Gen 1 `$43` cry, and a persistent Bag token that enables Wonder Guard for every active Shedinja. |
| Gold | 252 | Three-frame Crystal-style front animation, static back art, normal/shiny palettes, a two-page Dex entry, intrinsic enemy Wonder Guard, and held-item player activation. |

Gold’s `WONDER_GUARD` is a non-usable normal Bag item so it can be equipped through the game’s ordinary **GIVE** action. After the Mystery Egg return, Elm’s assistant preserves the native five Poké Balls and then awards a level-5 Shedinja holding it. That item enables the Gold route encounters only when an owned Shedinja in the party or PC boxes is holding it. Enemy Shedinja receives the ordinary-damage protection intrinsically, while the player’s active Shedinja requires the held item. In Red/Blue/Yellow, the token stays in the Bag because that generation has no held-item system; while present, it enables Wonder Guard for every active Shedinja on either side. In either game, the rule blocks only direct non-super-effective move damage; it never protects other Pokémon, an inactive party member, status moves, or typeless self-damage such as confusion.

`ELEC TERA ORB` and `AIR BALLOON` are permanent battle-only player options. They work only for the player’s active Shedinja, do not consume a turn, may each activate once per field entry, and clear when Shedinja switches out or the battle ends. The Orb temporarily uses Electric as that active Shedinja’s defensive type; the Balloon makes Ground moves miss before damage. Gold’s player Shedinja must still hold `WONDER_GUARD` for Wonder Guard itself—the Orb changes that existing protection’s defensive matchup rather than bypassing the held-item requirement.

## Wild encounters

| Game | Locations | Chance | Level range |
|---|---|---:|---:|
| Red / Blue / Yellow | Route 1, Route 4, Victory Road | 5%, 7%, 10% | 3–5, 10–12, 36–38 |
| Gold | Route 29, Route 34, Victory Road; active only while an owned Shedinja holds `WONDER_GUARD` | 5%, 7%, 10% | 3–5, 10–12, 36–38 |

> **Compatibility guidance:** The single **Shedinja Compatibility Bridge** supports both framework paths. With Crystal 251 in Red, Blue, or Yellow, it moves Shedinja to Crystal-safe index `252` and supplies Crystal runtime metadata. With Expanded Species in Gold, it preserves Shedinja’s framework-aware #292 identity and presentation. The bridge is inert without either framework. Kanto Reforged and unrelated roster/Dex/index-overhaul mods remain unsupported without their own dedicated compatibility bridge.

## Package migration

Shedinja 0.3.0 corrects the package and manifest ID from the misspelled **`shedninja`** to **`shedinja`**, and moves the public repository to `inmento/Shedinja`. Because Gen1Recomp identifies installed mods by manifest ID, remove the old `shedninja` installation and install `shedinja-0.3.0.zip` once. Install Shedinja Compatibility Bridge 0.1.4 afterward if you use an expansion framework; future launcher updates then follow the corrected identity.

## Sprite artwork attribution

The Gen 1 sprites are adaptations of **“G1SP 0292 – Shedinja”** by **BouncingPiplup**, under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The Gold front animation and back sprite are adapted from **“GSC Shedinja”** by **nuukiie** (Nuuk), used for non-commercial purposes with credit under the artist’s stated terms. See the repository’s `CREDITS.md` for complete source links and adaptation details.

[View the source repository](https://github.com/inmento/Shedinja) or [download the current release](https://github.com/inmento/Shedinja/releases/latest).
