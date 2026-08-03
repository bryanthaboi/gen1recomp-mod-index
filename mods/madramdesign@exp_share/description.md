# Exp Share

Always-on party experience for Gen1Recomp — Gen 6+ Exp Share or classic
**EXP.ALL** math, without needing Oak's Aide item.

## Modes

| Mode | Behavior |
| --- | --- |
| **MODERN** | Full undivided EXP to every living party Pokémon. Needs a build with `BattleState.awardExp` / `battle.exp_award` (newer than 0.1.38). |
| **CLASSIC** | Gen 1 EXP.ALL share math without the bag item. |
| **OFF** | Vanilla. |

On **0.1.38** (no `awardExp`), the mod forces classic EXP.ALL so sharing still
works — bench Pokémon get “with EXP.ALL” messages.

**EXP MESSAGES:** EVERYONE / FIGHTERS / SILENT.

## Install

1. Download `exp_share-1.0.2.zip` from [Releases](https://github.com/madramdesign/gen1recomp-exp-share/releases).
2. Gen1Recomp → **F10** → **Import mod .zip**.
3. Enable **Exp Share**, then fully quit and relaunch.

## Compatibility

- Mod API 2, engine `>=0.1.0 <2.0.0`.
- `content` profile; `affects_link: false`.
- Stacks fine with Battle EXP Bar (HUD only). Not the same as Pokewalker.

## Credits

madramdesign · MIT
