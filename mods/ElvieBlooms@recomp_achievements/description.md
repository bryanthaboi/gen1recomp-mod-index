# Recomp Achievements

Achievements for every game gen1recomp plays: Red, Blue, Yellow, Gold, Silver, Crystal, Ruby, Sapphire, Emerald, FireRed and LeafGreen. That's all 1003 entries from the lists RetroAchievements publishes, each checked by this mod's own logic as you play. Unlocks are saved in your game, so they follow Save Sync, and nothing goes online.

An unofficial fan project, not affiliated with RetroAchievements. Unlocks here don't count on retroachievements.org.

## What you get

- **Old saves count.** Load a save you've been playing, imported cartridge saves included, and everything it can prove unlocks in one WELCOME BACK popup: badges, story, Pokédex, items, cleared areas.
- **TROPHIES** on the START menu (**TROPHY** in Gen 1 and Gen 2), with filters for Earned, Missing, In progress and **Missable**, and a page on how each one is checked.
- Unlock popups, an optional jingle, and small progress cards ("3 / 50").
- Themes, and a **CLASSIC MENU** drawn in each game's own style: the text box in Gen 1 and Gen 2, the game's windows and font in Gen 3.
- **Challenges** for the Set Mode entries: set OPTION > BATTLE STYLE to SET and stick to the limits on the achievement's page. They're judged while you play, so they count from when the mod is installed.
- An optional leaderboard, with a separate **Extra Credit** board for bonus and mod achievements. The mod never goes online: you copy a short card from the game into the site or the Discord bot.

## For mod makers

Your mod can add its own achievements, report progress and listen for unlocks. They show up in the same menu, with a tab for your mod. Make it an optional dependency and your mod still loads without this one. The contract is `docs/PROVIDER_API.md`, with a complete example mod in the repo.

## What it changes

One START menu row, popups drawn over the game, and its own records under `modData.recomp_achievements` in the save. Nothing else: no species, moves, items, maps, scripts or battles are touched. The details are in `DIFFERENCES.md`.

## Install

1. Download `recomp_achievements-2.6.2.zip` from the releases page.
2. In the launcher, MODS > **Import mod .zip**.
3. Enable it for the games you play and load a save.

The launcher's **Update** and **Versions** take it from there.

## Compatibility

- Mod API 3, gen1recomp `>=0.3.97`, all eleven games.
- Pure `content` profile: link play is unaffected.
- Declares `engine_internals`. Nothing is patched: the Gen 3 **CLASSIC MENU** borrows the game's window and font drawing, which the modding API doesn't offer yet, and falls back to the modern menu if that ever moves.
- If another mod replaces your START menu, turn **START MENU ENTRY** off and open the menu with **OPEN TROPHIES** in the Mods manager.

## Credits

Achievement titles, descriptions and point values are by RetroAchievements and each achievement's author, credited in the game; their trigger logic isn't used. Flag, trainer and item names come from the pret disassemblies (pokered, pokegold, pokecrystal, pokefirered, pokeemerald, pokeruby). Fixes ported from Shane McGovern's (Nexhas28) Emerald Lens contributions. Code by Elvie, MIT licensed.
