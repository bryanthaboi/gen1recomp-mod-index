# Event Soundbytes

A [Gen1Recomp](https://github.com/bryanthaboi/gen1recomp) mod that plays a voice line when the player starts a New Game or Continues an existing save, with the music briefly ducking underneath each line.

Built as a companion to the [Crystal](https://github.com/dburton95/crystal) player mod — the voice lines are Kris's lines from *Pokémon Masters EX*, so if you're already using Crystal to look the part, Event Soundbytes gives her a voice to match. It works fine on its own too, without Crystal installed.

## Features

- A single fixed voice line plays on **New Game**
- One of three random voice lines plays on **Continue**, so reloading a save doesn't feel identical every time
- Background music ducks briefly while a line plays, so it isn't buried
- Works on Gen 1 (Red/Blue/Yellow) and Gen 2 (Gold)

## Installation

1. Download the latest release `.zip` from the [Releases](../../releases) page.
2. In-game: **MODS → Import mod .zip**, or extract manually into your Gen1Recomp `mods/` folder:
   - Windows: `%APPDATA%\love\pokemon-love2d\mods\`
   - macOS: `~/Library/Application Support/LOVE/pokemon-love2d/mods/`
   - Linux: `~/.local/share/love/pokemon-love2d/mods/`
3. Restart the game.
4. Open the **MODS** panel and confirm **Event Soundbytes** shows as `ENABLED`.

## How it works

Gen1Recomp doesn't expose a hook that fires directly on a title-screen button press, so this mod listens for:

- `intro.oak_speech.finished` — fires once the player finishes the New Game naming/intro sequence
- `save.loaded` — fires after an existing save is read and validated (Continue)

Music ducking hooks `music.volume` and briefly scales it down for a couple of seconds after either line starts.

## Assets

Sound files live in `assets/` and aren't tracked as placeholders in this repo structure — replace them with your own if you fork this:

- `assets/new_game.ogg` — plays on New Game
- `assets/continue1.ogg`, `assets/continue2.ogg`, `assets/continue3.ogg` — random pool for Continue

## Known limitations

- Voice lines are shared across all party/player customization — no per-save or per-character variant selection yet.
- No in-game toggle yet to disable the sounds without removing the mod.
- Jessie character option only has a new game voice line and it's Kris's. For now it's a place holder and all other events are silent with Jessie selected.

## Credits

- Voice lines: Kris, *Pokémon Masters EX* (DeNA / The Pokémon Company)
- Built to pair with [Crystal](https://github.com/dburton95/crystal) by dburton95

## Contributing

Forks and collaboration are welcome — whether that's swapping in your own voice lines, hooking additional events, or general improvements. Feel free to open a PR or an issue.
