# OmniQoL

**OmniQoL** is an all-in-one, modular Quality of Life (QoL) suite built for Pokémon engine recreations, targeting [bryanthaboi/gen1recomp](https://github.com/bryanthaboi/gen1recomp).

Every feature is designed as an independent module that can be turned on or off directly within the game's Options menu (`OMNIQOL`), with preferences saved per save file.

---

### 🏃 Module 1: Running Shoes (Pokémon Red, Blue & Yellow)
- **Hold B to Run**: Doubles player overworld movement speed (from 16 to 8 frames per tile, matching the Bicycle).
- **Pikachu Follower Synchronization (Yellow)**: Pikachu automatically matches player running speed (8 frames/tile), with a 4 frames/tile catch-up sprint if separated or turning corners. Happiness and mood step tracking function normally.
- **Usable Everywhere**: Full movement freedom indoors, outdoors, in caves, buildings, and the Safari Zone.
- **Fair Encounter Rates**: Standard walking encounter rates are preserved (no extra encounter penalty).
- **Scripted Cutscene & Escort Protection**: Automatically restores vanilla step duration when idle and during NPC escorts (e.g., Professor Oak escorting the player to the lab) to prevent cutscene desyncs.
- **State Preservation**: Normal Bicycle and Surfing speeds are preserved.

### ⚙️ Native Options Menu Integration (`OMNIQOL`)
- Injects an `OMNIQOL` entry directly into the native **Options Menu** (`OPTION`), accessible both in the overworld and on the Title Screen.
- Custom interactive UI screen allows toggling modules `[ON ]` or `[OFF]` at any time with an authentic Pokémon arrow cursor.
- Leaves the overworld Start Menu pure vanilla.
- Settings are saved **per save file** during gameplay, and saved as **global defaults** when configured from the Title Screen.

---

### 🗺️ Multi-Game Rollout Roadmap
For each module, development follows a structured multi-generation sequence:
- [x] **Gen 1**: Pokémon Red & Blue *(Complete)*
- [x] **Gen 1**: Pokémon Yellow *(Complete)*
- [ ] **Gen 2**: Pokémon Gold & Silver ➔ Pokémon Crystal *(Next Target)*
- [ ] **Gen 3**: Pokémon FireRed & LeafGreen ➔ Pokémon Ruby & Sapphire ➔ Pokémon Emerald

---

### 🔗 Links & Source Code
- **Repository**: [https://github.com/swissguy/OmniQoL](https://github.com/swissguy/OmniQoL)
- **Releases**: [https://github.com/swissguy/OmniQoL/releases](https://github.com/swissguy/OmniQoL/releases)
