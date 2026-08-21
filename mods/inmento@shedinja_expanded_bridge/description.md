# Shedinja Compatibility Bridge

**Shedinja Compatibility Bridge** is the single optional companion for [Shedinja](https://github.com/inmento/Shedinja). It checks the active game and supported framework, then applies only the compatibility path that belongs to that configuration.

| Configuration | Result |
|---|---|
| Red, Blue, or Yellow with Crystal 251 | Moves Shedinja from Crystal’s occupied index 152 to Crystal-safe index **252**, retains visible National Dex **#292**, and supplies split-stat plus genderless metadata. |
| Gold with Expanded Species | Restores Shedinja’s framework-aware virtual and visible **#292** identity, palette, party icon, and sparse OLD/National Pokédex ordering. |
| Neither optional framework active | The bridge remains inert and core Shedinja keeps its normal standalone behavior. |

Core Shedinja **0.3.0+** is required. This release uses the corrected `shedinja` package ID; users migrating from the retired `shedninja` ID must remove the old installation and install Shedinja 0.3.0 once. Crystal 251 and Expanded Species are optional, game-scoped integrations rather than required dependencies. Install the appropriate framework only for the game you are playing.

> The former **Shedinja Crystal 251 Bridge** is retired. Remove or disable it before installing this unified bridge; do not enable both bridge mods together.

The bridge contains no art files. Core Shedinja retains responsibility for sprite attribution and included credits.
