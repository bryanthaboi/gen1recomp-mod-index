# Kanto Gear

A DS-inspired Pokégear and C-Gear companion for Pokémon Gen 1–3 in
Gen1Recomp. Keep your game on one screen and maps, team, notes and progress
close at hand, using touch or a mouse.

Supports **Red, Blue, Yellow, Gold, Silver, Crystal, Ruby, Sapphire,
FireRed, LeafGreen and Emerald** on Android, Windows and Linux.

## Choose your screen setup

- **Fullscreen Swap:** switch between the game and Gear on one screen.
- **Combined:** stack both views, place them side by side or use a corner overlay.
- **Separate:** use a dual-screen handheld or independent desktop windows.
- **Phone / Browser:** pair a browser on your local Wi-Fi as an optional Gear
  display, with optional touch controller buttons. This mode is experimental.

Choose Pokégear or C-Gear, each with Light, Dark and Auto variants. Arrange
Home pages with apps and widgets, and enable optional apps in Silph Store.
Compatible apps from other installed Recomp mods can appear in the Store too.

## Apps and controls

- **Explorer and Map:** live local maps, encounters, trainers, items, hidden
  finds, regional navigation and available Fly destinations.
- **Party, Bag and Pokédex:** partner summaries, held items, contextual item
  actions, complete Dex entries, evolutions and habitats.
- **Stamps and Notes:** location completion, remaining goals, text notes,
  checklists and drawings.
- **Day-Care and Calendar:** boarded partners, breeding information where
  supported, weekly events in Gen 2 and game-specific activities in Gen 3.
- **Pokégear and PokéNav:** install the game's original device as a Store app
  in its supported games. Walk with the game's controls above while using the
  device through touch below, or add widgets that open individual sections.
- **Field Kit, Trainer Card and Step Counter:** currently usable field tools,
  trainer records, badges and movement tracking.
- **Battle controls:** Companion, Info, Gear and Full Gear layouts, including
  supported Gen 3 double battles. Native menus also gain matching touch pages.
- **Silph Connect:** player presence through Recomp's shared connection.
  Friends, chat and battle/trade invitations are not available.

Discovery presets let you choose original-game information, guidance or all
available data, with individual switches for a custom setup. English, German,
Spanish (Spain), French, Japanese and Italian UI catalogs are included; some
newer labels fall back to English.

## Install and requirements

Install from the Mod Index or import the ZIP from the
[latest release](https://github.com/AverageConsumer/kanto-gear/releases/latest),
enable Kanto Gear and open its Options. The same ZIP works on all three host
platforms. It includes no ROM or save; bring your own supported game ROM.

Kanto Gear 4.4.0 requires **Gen1Recomp 0.3.93 or newer (mod API 3)**.
Update Recomp before installing this version. Hosts on 0.3.92 or earlier should
keep Kanto Gear 4.3.1 until updated. Gen 3 welcomes broader playthrough testing;
some specialized native screens remain on the game screen.

Permissions match the mod manifest:

- `engine_internals`: native game integration, companion controls and display routing.
- `network`: optional local phone transport and integration with Recomp's online client.
- `compute`: worker threads for phone pairing and video processing.

Phone mode uses an **unencrypted local connection**. Pair only on a private
network you trust, and do not expose its port to the internet. One-time pairing
credentials expire after five minutes. Open Gear content, including notes, is
visible to the paired browser. Native online arena restrictions still apply.

## Support and contributions

See the [repository](https://github.com/AverageConsumer/kanto-gear) for screenshots,
the full feature guide and development documentation. Report problems through
the [bug form](https://github.com/AverageConsumer/kanto-gear/issues/new?template=bug_report.yml)
with your game, device, versions, display mode and reproduction steps.
Use the [translation form](https://github.com/AverageConsumer/kanto-gear/issues/new?template=translation.yml)
for wording corrections and the
[security policy](https://github.com/AverageConsumer/kanto-gear/blob/main/SECURITY.md)
for private vulnerability reports.

Kanto Gear is an independent fan project under the MIT License, with separate
notices for bundled fonts and libraries. It is not an official Gen1Recomp or
Pokémon product.
