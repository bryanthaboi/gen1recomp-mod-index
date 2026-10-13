# GB-Link Online Trades

Trade Pokémon at the Cable Club with a **real Game Boy** on a GB-Link
adapter, an emulator (BGB), or another copy of gen1recomp, over the
internet. Everyone uses the same five-digit rooms as
[pokemon.gblink.io](https://pokemon.gblink.io).

For **Red, Blue and Yellow** (mod API 2). Experimental.

## How to trade

1. Enable the mod and talk to the Cable Club receptionist at any Pokémon
   Center. Say YES to the save, then pick **GB-LINK ONLINE**.
2. Enter a room number. The other player enters the same number:
   - pokemon.gblink.io → *Gen 1* → *Link Trade* (real Game Boy or BGB)
   - Lorenzooone's PokemonGB Online Trades client 4.x, link trade, Gen 1
   - another copy of gen1recomp with this mod
3. When they sit down at the Trade Center table, gen1recomp opens its own
   Trade Center. Pick, check STATS, confirm. Trade evolutions, the trade
   animation and the autosave all work as on a real cable. You can make
   several trades in one visit.

## Notes

- It speaks the PokemonGB online trade protocol 4.1 (sync and buffered
  modes) directly. No emulator runs inside the game.
- It uses ws:// only, because this build has no TLS. The default server is
  the public one at `ws://pokemon-gb-online-trades.herokuapp.com`. You can
  change it with the **SERVER** mod option.
- The protocol aborts a trade if a byte is 0.8 s late. It is comfortable up
  to about 300 ms each way.
- The Colosseum (battles) is not offered. A GBA running FireRed or
  LeafGreen cannot link with Red and Blue directly.

Permissions: `network` (the trade server) and `engine_internals` (it opens
the Cable Club's link screen and adopts the engine's own Trade Center).
