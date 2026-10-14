# GB-Link Online Trades

Trade Pokémon with a **real Game Boy** on a GB-Link adapter, an emulator
(BGB), or another copy of gen1recomp, over the internet. Everyone uses the
same five-digit rooms as [pokemon.gblink.io](https://pokemon.gblink.io).

For **Red, Blue, Yellow, Gold, Silver and Crystal** (mod API 2). Experimental.

## How to trade

**Red, Blue, Yellow.** Talk to the Cable Club receptionist at any Pokémon
Center, say YES to the save, then pick **GB-LINK ONLINE** and enter a room
number. When the other player sits down, gen1recomp opens its own Trade
Center: pick, check STATS, confirm. Trade evolutions, the animation and the
autosave all work as on a real cable, and you can make several trades in
one visit.

**Gold, Silver, Crystal.** Talk to the Trade Center receptionist upstairs in
any Pokémon Center and answer YES. Instead of waiting for a cable she opens
**GB-LINK ONLINE**: enter the room number. The cart's own script then saves,
walks you in, and the table works like the cart's: STATS, TRADE, the
confirm, the trade animation, trade evolutions (Everstone and held-item
rules), mail travelling with its Pokémon, and the autosave.

The other player enters the same number:

- pokemon.gblink.io → *Gen 1* (Red/Blue/Yellow) or *Gen 2*
  (Gold/Silver/Crystal) → *Link Trade* (real Game Boy, or BGB)
- Lorenzooone's PokemonGB Online Trades client 4.x, link trade, the
  matching generation
- another copy of gen1recomp with this mod

A Gold/Silver/Crystal *cartridge* can also reach Red/Blue/Yellow here
through its own Time Capsule.

## Notes

- It speaks the PokemonGB online trade protocol 4.1 (sync and buffered
  modes, Gen 1 and Gen 2) directly. No emulator runs inside the game.
- The default server is the public one at
  `ws://pokemon-gb-online-trades.herokuapp.com`; change it with the
  **SERVER** mod option. `wss://` works on builds with the engine's TLS
  dialer (official Windows builds, Android); elsewhere use `ws://`.
- The protocol aborts a trade if a byte is 0.8 s late. It is comfortable up
  to about 300 ms each way.
- Battles (the Colosseum) are not offered, nor is gen1recomp's own Time
  Capsule desk on Gold/Silver/Crystal.
- Tested live against Red, Blue, Yellow and Gold cartridges in BGB, both
  saves checked with PKHeX after each trade.

Permissions: `network` (the trade server) and `engine_internals` (it opens
the Cable Club's link screen on Gen 1, the Trade Center desk's cable steps
on Gen 2, and the engine's own trade screens).
