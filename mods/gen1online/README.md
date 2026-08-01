# Pokemon Gen 1 Recomp - Overworld Co-Op Online Mod

A real-time multiplayer overworld exploration and online distance-based link battle mod built for the **Pokemon Gen 1 Recomp Project**.

---

## 🌟 Key Features

- **🌐 Public Server Relay Hosting**:
  - Host or join online multiplayer sessions worldwide using 6-character Room Codes (e.g. `X7K9P2`) over the official public relay server (`147.182.215.255:7778`).
- **🏠 Local Area Network (LAN) Hosting**:
  - Direct P2P LAN connection support with built-in 12-digit IP scrubber interface (`PORT: 7777`).
- **👥 Dual Overworld Sprite Syncing**:
  - Synchronizes both Player 2's Human Trainer avatar (`RED`) and Player 2's trailing Follower Pokémon in real-time.
  - Safe modular fallback: If the follower mod is omitted, the human trainer avatar continues to render seamlessly with zero errors.
- **✨ Smooth 60 FPS Movement & Walking Animations**:
  - Continuous linear interpolation (Lerp) eliminates tile teleporting.
  - Directional facing and step-flip leg walking animations.
  - 48px map warp threshold ensures clean transitions when changing zones.
- **🚧 Solid Physical Collisions & Spawn Nudge**:
  - Players and follower Pokémon cannot walk through each other (`passable = false`).
  - Automatic same-tile spawn nudge moves connecting players to the next free adjacent cell if they spawn on the exact same tile.
- **⚔️ Distance-Based Online Link Battles**:
  - Interact with another player on the overworld and select **`PVP LINK BATTLE`** to challenge them over the network.
  - Uses the official Recomp lockstep `LinkBattle` engine with 3D camera support, move animations, PP/HP tracking, and battle logic.
- **🏥 Background Pokemon Center Pre-Battle Heal**:
  - Automatically restores full HP, cures status conditions, and refills move PPs prior to starting a PVP Link Battle.
- **💾 Forced Save & Disconnect Protection**:
  - Executes a forced game save before initiating any online or LAN connection.
  - If a player disconnects or connection drops, displays a notification, saves the game, and reloads the current map cleanly in single-player mode.
- **🎮 Authentic Game Boy UI HUD**:
  - Displays room code and connection status in a clean Game Boy text frame in the top-right corner.
- **🧊 3D Voxel Diorama Compatible**:
  - Fully compatible with `DramaticShapeVoxelMod` and 3D camera rotation.

---

## 📥 Installation

1. Download or clone this repository folder into your Recomp `mods/` directory:
   ```text
   pokemon-gen1-recomp-project/mods/overworld_coop/
   ```
2. Ensure `overworld_coop` is enabled in your mod settings menu or `options.lua`.

---

## 🎮 How to Play

### Hosting an Online Room:
1. Press **`START`** on the overworld to open the Start Menu.
2. Select **`CO-OP ONLINE`** → **`HOST SERVER`**.
3. Your game will save, connect to the relay server, and generate a 6-character **ROOM CODE** in the top-right corner.
4. Share the Room Code with your friend!

### Joining an Online Room:
1. Press **`START`** → **`CO-OP ONLINE`** → **`JOIN SERVER`**.
2. Use D-Pad Up/Down to scrub characters and D-Pad Left/Right to select slots.
3. Press **`A`** to join the room!

### Hosting/Joining LAN:
- Select **`HOST LAN`** to host locally on port `7777`.
- Select **`JOIN LAN`** to enter the host's local IP address (`192.168.X.X`).

### Starting a PVP Link Battle:
1. Walk up to Player 2 on the overworld map and face them.
2. Press **`A`** to interact.
3. Select **`PVP LINK BATTLE`**.
4. Player 2 will receive a challenge prompt (`ACCEPT BATTLE` / `DECLINE`).
5. Upon acceptance, both players enter the online Link Battle arena!

---

## 📜 License

Distributed under the MIT License. See project root for details.
