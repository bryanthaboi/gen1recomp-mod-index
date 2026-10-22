# PkMultiplayer — online co-op for Gen2Recomped

Two players, one Johto. Play **Gold, Silver or Crystal** (and Red/Blue/Yellow)
with a friend in the same world.

## Features

| | |
|---|---|
| Shared world | your partner walks on your map, with their name above them |
| Chat | **T** (also during a double battle); on phones, START → CO-OP (LAN) → CHAT |
| Emotes | **Y**; with your own ROM imported (optional), the cartridge's own bubbles |
| Double battles | trainers become 2-vs-2 doubles in lockstep, with HeartGold/SoulSilver's doubles rules and an enemy AI built for doubles |
| Shared story | events one player lives, the other lives too; big battles ask both first |
| Extras | Cable Club trades, P1 vs P2, items for your partner's Pokémon, shared Bug-Catching Contest, Hall of Fame and clock |
| Warp | only to towns you have visited, your partner must accept, 10-minute cooldown |

## How to play

1. Both players install the mod (same version) and enable it in **MODS**.
2. One player: START → **CO-OP (LAN)** → **HOST**. The other: **JOIN** with the host's IP.
3. Over the internet, join the same [ZeroTier](https://www.zerotier.com/) network and use the host's ZeroTier IP. Port **7777**.

From the title screen you can also pick **NEW CO-OP GAME** or **CONTINUE CO-OP**.

## Notes

- **Gen 1 and Gen 2 only.** In other games the mod loads and does nothing.
- **Permissions:** `network` (the co-op link, ENet/UDP) and `engine_internals`
  (it edits about a hundred engine functions).
- The mod ships **none of the engine's code and no ROM data**: it carries
  context-hashed edits that are applied at load time to your own copy of the
  game. If an engine update moves a function too far, that module is left
  unpatched and `log.txt` says so.
- Logs for bug reports: `coop.log` and `log.txt` in the game's save folder.

Source, tests and issues: https://github.com/Mochx-007/PkMultiplayer
