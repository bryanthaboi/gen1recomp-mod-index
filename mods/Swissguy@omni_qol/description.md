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

### 🎓 Module 2: EXP Share (Pokémon Red, Blue & Yellow)
- **Modern Gen 6+ EXP Distribution**: Active battlers receive a full 100% EXP share each (Gen 8+ style, no switching dilution), while non-fainted benched party members receive 50% EXP. Fainted Pokémon receive 0 EXP.
- **Full Stat EXP (Gen 6+ style)**: All party members earning EXP receive 100% of the defeated enemy's base stats as Stat EXP (EVs) across all 5 stats.
- **Streamlined Announcements**: Active battlers display standard dialogue; benched party members are cleanly announced via a single consolidated prompt (`"The rest of the team gained EXP!"`), eliminating repetitive dialogue boxes.
- **Native Level-Up Sequencing**: Any Pokémon that levels up immediately triggers its level-up fanfare, stat growth box, and move-learning dialogue. In Pokémon Yellow, Pikachu also gains happiness upon leveling up.
- **Pure Software Toggle**: Enabled by default, occupying 0 Bag inventory slots.

### 🔄 Module 3: Trade Evolutions (Pokémon Red, Blue & Yellow)
- **Level 40 Evolution**: Kadabra, Machoke, Graveler, and Haunter evolve naturally into Alakazam, Machamp, Golem, and Gengar upon reaching or gaining a level at Level 40+.
- **Level 100 Support (Gen 8+ Style)**: Using a Rare Candy on a Level 100 Pokémon triggers the evolution sequence without exceeding Level 100.
- **B-Button Cancellation**: Preserves authentic level-up behavior; players can cancel the evolution by pressing B during the sequence.
- **Trade Coexistence**: Traditional link-trading continues to trigger evolution normally.
- **Vanilla NPC Trades**: In-game NPC trades (e.g., Machoke in Pokémon Blue/Yellow) do not immediately auto-evolve upon receipt; they evolve upon their next level-up to 40+.

### ✨ Module 4: Catch All 151 Pokémon (Pokémon Red, Blue & Yellow)
- **Wild Starters**: Bulbasaur, Charmander, and Squirtle appear in the wild in thematic habitats across Kanto.
- **Cross-Version Exclusives**: All missing and version-exclusive Pokémon from Red, Blue, and Yellow are catchable across all three games in counterpart routes.
- **Safari Zone Exclusives Outside Safari Zone**: Chansey, Kangaskhan, Tauros, Scyther, Pinsir, Dratini, and Tangela spawn in overworld routes for standard battles and captures with regular Pokéballs.
- **Mutually Exclusive & Single-Choice Pokémon**: Wild encounters for unchosen fossils (Omanyte/Kabuto), Dojo fighters (Hitmonlee/Hitmonchan), wild Eevee (enabling all 3 Eeveelutions), and trade-only species (Jynx, Farfetch'd, Mr. Mime, Lickitung, Porygon).
- **Immediate Legendary & Snorlax Respawns**: Articuno, Zapdos, Moltres, Mewtwo, and Snorlax immediately respawn upon exiting and re-entering their room or map if defeated or fled without catching.
- **Mythical Mew Encounter**: Stationary interactable Lv. 50 Mew rests on the deepest floor of Cerulean Cave (Unknown Dungeon B1F) with authentic cry and battle sequence, respawning on room re-entry if not caught.
- **Celadon Department Store Moon Stone**: Sold on 4F (Wiseman Gifts) alongside Fire, Water, Thunder, and Leaf Stones at standard ¥2,100 with infinite stock, ensuring Moon Stone evolutions are never blocked.
- **Options Menu Integration**: Toggleable on/off anytime under `OPTION ➔ OMNIQOL` (`CATCH 151`), enabled by default.

### 🧠 Module 5: Move Relearner (Pokémon Red, Blue & Yellow)
- **Every Pokémon Center Across Kanto**: A distinguished Gentleman Move Reminder NPC appears in the lobby of all 12 Pokémon Centers (Viridian, Pewter, Cerulean, Vermilion, Lavender, Celadon, Fuchsia, Saffron, Cinnabar, Indigo Plateau, Route 4, and Route 10).
- **Free to Use**: Zero Pokédollar or item cost (Sword & Shield style).
- **Missed Pre-Evolution Moves**: Any Pokémon can relearn all level-up moves their current species and any earlier stages in their evolutionary line could have learned up to their current level (remedying early stone/trade evolutions).
- **Level 1 Base / Starting Moves**: Relearn any initial starting move at any level.
- **TM Tutor Mode (`RELEARN + TMS`)**: Teaches any compatible TM01–TM50 moves, including inherited compatibility from pre-evolutions.
  - HM moves (Cut, Fly, Surf, Strength, Flash) remain excluded from TM tutoring.
- **Interactive Move Replacement**: Teaches directly if fewer than 4 moves are known, or opens an interactive replacement screen.
- **Scrollable Party & Move Lists**: Full 6-Pokémon party support and move lists with windowed scrolling and indicator arrows.
- **3-Way Options Menu Integration**: Toggled directly under `OPTION ➔ OMNIQOL` (`RELEARNER`):
  - `[OFF]`: Disabled.
  - `[RELEARN]`: Natural level-up moves and pre-evolution moves.
  - `[REL+TMS]`: Natural level-up moves + all compatible TM01–TM50 moves.

### ✂️ Module 6: Forget HM Moves (Pokémon Red, Blue & Yellow)
- **Freely Overwrite HM Moves**: Allows overwriting and forgetting HM moves (Cut, Fly, Surf, Strength, Flash) whenever learning any new move (via Level Up, TM items, or Move Relearner).
- **Eliminates Trapped Movesets**: Removes the permanent HM lock present in vanilla Gen 1.
- **Dedicated Toggle**: Separately toggleable under `OPTION ➔ OMNIQOL` (`FORGET HMS`), enabled by default.

### ⚙️ Native Options Menu Integration (`OMNIQOL`)
- Injects an `OMNIQOL` entry directly into the native **Options Menu** (`OPTION`), accessible both in the overworld and on the Title Screen.
- Custom interactive UI screen allows cycling module values (e.g., `[ON ]`/`[OFF]` or `[RELEARN]`/`[REL+TMS]`/`[OFF]`) with an authentic Pokémon arrow cursor.
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
