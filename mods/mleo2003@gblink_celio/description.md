# GB-Link Celio Trades

Trade Pokémon from **FireRed or LeafGreen** with a **real GBA** on a Celio
(GB-Link) adapter or **mGBA (Celio edition)**, over the internet, in the
same four-digit rooms as [celio.gblink.io](https://celio.gblink.io).

For **FireRed and LeafGreen** (mod API 2). Experimental.

## How to trade

Go upstairs in any Pokémon Center, talk to the **Cable Club** attendant,
choose **TRADE CENTER** and save. The **GBA LINK ONLINE (CELIO)** door
opens: **MAKE A ROOM** shows a number for your friend, or **JOIN A ROOM**
takes theirs.

Your friend opens celio.gblink.io → *Online Link*, joins (or creates) the
room, connects their GBA or mGBA, and on their game talks to the Cable Club
attendant, picks TRADE CENTER and saves. From there it is an ordinary cable
trade on both sides: sit down, and gen1recomp's own Trade Center opens with
their party: STATS, TRADE, the confirm, the animation, trade evolutions and
the save. Trade as often as you like; after both cancel you are back in the
room, and when either player walks out the other is shown out too.

## Notes

- gen1recomp commits a trade only after the other game has saved its side,
  so a dropped connection leaves both games as they were. The other game
  animates and saves first, then yours.
- The Celio server is wss:// only: it needs the game's TLS helper (the
  official Windows and Android builds have it).
- Two copies of gen1recomp cannot meet over Celio (both would lead the
  link); use the game's own online play for that.
- Live-tested against FireRed in mGBA Celio edition (both saves checked
  with PKHeX). LeafGreen, real adapters and Ruby/Sapphire/Emerald partners
  are not tested yet.
- Source and releases: [mleo2003/gen1recomp-celio](https://github.com/mleo2003/gen1recomp-celio).
