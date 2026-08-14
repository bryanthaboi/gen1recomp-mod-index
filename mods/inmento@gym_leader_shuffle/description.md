# Gym Leader Shuffle

Gym Leader Shuffle creates a persistent per-save derangement of the eight Kanto Gym Leaders. The visiting leader supplies the overworld sprite, portrait, introductory dialogue, and a team scaled to the physical gym. The gym itself retains its original badge, TM, rewards, defeat wording, progression flag, and trainer-deactivation behavior.

## What it changes

Each new mapping assigns every Kanto Gym Leader to a different gym, with no leader remaining in their original gym. The visiting leader’s team is adjusted to the destination gym’s level curve, including evolution or de-evolution where necessary.

When enabled, SHUFFLE GYM TRAINERS applies the visiting leader’s non-leader gym-trainer roster to that gym while preserving its intended level curve. RANDOMIZE MOVE SETS, PREFER GYM-TYPE MOVES, ALLOW NATIVE STAB MOVES, and ENSURE A DAMAGING MOVE control the optional move-set generator.

OPEN SPOILER LOG displays the eight saved leader-to-badge assignments. GYM TELEPORT (TEST) and RETURN TO LAST POINT (TEST) are one-shot testing utilities for navigating the next eligible gym and returning to the original location. Giovanni’s Rocket Hideout and Silph Co. appearances are not shuffled; only his Viridian Gym appearance participates.

## Install

Download `gym_leader_shuffle-0.0.1.zip` from the source repository’s Releases page. In Gen 1 Recomp, open MODS and select Import mod .zip. Enable the mod and start a New Game, or load a save before entering a Kanto gym to create its persistent mapping.

## Compatibility

Gym Leader Shuffle uses Mod API 2 with the `content` profile and does not affect link play. It has no declared dependencies or conflicts. It contains no ROM-derived content.

## License

Gym Leader Shuffle is distributed under the MIT License. See the source repository for the full license text.
