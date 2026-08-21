# Blackjack Corner

Blackjack Corner turns Pokémon Gen 1 into a Kanto-wide casino campaign. Its
optional, save-scoped Gamble Mode remixes the adventure from Oak's Lab through
all eight Gyms and a Rocket-run endgame, while its casino network remains
available when Gamble Mode is declined.

## What it adds

- Eight playable games: Blackjack, house-banked Texas Hold'em, Crash, Tube
  Flyer, Prize Case, animated Horse Racing, Plinko, and Pokémon battle betting.
- Casinos in Pallet Town, Celadon, and every Kanto city, with live tables,
  arcade machines, city-specific dialogue, original staff and patrons, local
  Pokémon prize counters, two-way coin exchange, and hidden coin pickups.
- Random player and rival starters, paid rerolls, and one persistent Gym reward
  case for every badge when Gamble Mode is enabled. Each Gym Case uses a
  distinct ten-prize pool themed around its leader.
- Prize-aware Gym Leader reactions for all 80 current Gym Case rewards. The
  exact comment changes with the prize, rarity, and leader personality, and
  appears only after safe delivery to the Bag, party, or PC.
- A shared High Roller campaign with five ranks, persistent statistics, rank
  rewards, story-safe badge gates, and reactive casino dialogue.
- Rocket credit, recoverable default consequences, Pokémon pawning, and a
  late-game underground arena with posted odds and animated house-owned fights.
- Eight post-Gym CASE ACE trainers whose independent mixed-reward cases and
  dialogue no longer copy the nearby Gym Leader, plus a Cinnabar investigation,
  a fixed Dragonite-versus-Mewtwo exhibition, and an irreversible choice to
  expose Rocket or become the house champion.
- A shared one-million-coin economy, expanded Pokémon and item prizes, shiny
  prize upgrades, rare TMs, Mew, Dragonite, Surfing Pikachu, and Master Balls.
- Native nickname prompts for Starter Roulette, case, and counter-redemption
  Pokémon, including rewards delivered directly to the PC.

## Casino economy

Every Pallet, Celadon, and regional clerk can buy casino coins or cash them out
at the symmetric original rate of 50 coins for ¥1,000. Bulk and MAX options
respect both the one-million-coin Coin Case and the native ¥999,999 wallet cap.
The same clerks offer a limited local Pokémon catalogue; Celadon's dedicated
Prize Room retains the complete selection.

## Settings and compatibility

The mod has a permanent options page for the Gamble Mode default, repeat table
introductions, reveal speed, and shiny presentation. The Gamble Mode question
appears before Oak so every new campaign makes an explicit choice.

Starter Randomizer coexistence preserves randomized encounters and trainers
while Gamble Mode owns its roulette. Nuzlocke 2's post-Oak setup also resumes
after Oak exits instead of leaving the new-game screen blank.

## Shiny compatibility

Blackjack Corner includes a Gen II-style shiny fallback with Crystal palettes,
entrance sparkles, a chime, battle markers, and a status-screen icon. Dedicated
shiny mods load first and keep control; the bundled fallback activates only
when no supported external shiny provider is enabled.

## Install

1. Download `blackjack_corner-0.7.4.zip` from the
   [releases page](https://github.com/martin2844/gen1recomp-blackjack-corner/releases).
   Use the named mod ZIP, not GitHub's source-code archives.
2. In Gen1Recomp, choose **MODS → Import mod .zip**.
3. Select the ZIP, enable **Blackjack Corner**, and start the game.
4. Start a new game and answer Oak's Gamble Mode prompt. Choosing **NO** keeps
   normal starter and Gym reward progression while retaining the Celadon
   casino expansion.

With `github` declared in the manifest, the launcher's **Update** and
**Versions** buttons handle later releases.

## Compatibility

- Mod API 2; engine `>=0.0.0-0 <2.0.0`.
- Pokémon Red and Blue are release-certified. Pokémon Yellow support is
  available but remains experimental.
- `content` profile; link play is unaffected.
- Declares `engine_internals` for gameplay and presentation hooks, and
  `filesystem` for locally generated shiny assets.
- No hard dependencies or declared conflicts.

## License and credits

Blackjack Corner is released under the MIT License. Its bundled shiny fallback
adapts Gen II Shiny Indicators by Deftones565 under an MIT grant; the complete
attribution and license text ship in `THIRD_PARTY_NOTICES.md`.
