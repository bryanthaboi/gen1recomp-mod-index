A large-scale content overhaul for Pokemon Red/Blue in Gen1Recomp, created by MarsCrowley.

Mars's Expanded Kanto keeps the original Kanto adventure recognizable while expanding it with new Pokemon, areas, quests, bosses, moves, rematches, tournaments, postgame stories, quality-of-life additions, and custom battle animations.
Highlights

    Expanded Regional Dex with later-generation Pokemon integrated into Kanto.
    New areas including Alabaster Town, Viridian Deepwood, Mt. Cinnabar, Indigo City, and more.
    New side quests throughout the main game and postgame.
    Reworked encounters, evolution methods, trades, gifts, shops, trainers, Gym teams, Elite Four content, and postgame bosses.
    Kanto Fighting Tournament.
    New and ported moves, including signature attacks with custom battle animations.
    Journal / Adventure Record tracking major events and player progress.
    Postgame legendary quest lines.
    Compatibility work for several popular presentation and sprite mods used during development.

For a more complete list of intentional changes from vanilla, see DIFFERENCES.md.
Requirements

    A current Gen1Recomp build with mod API 2.
    Pokemon Red/Blue imported through Gen1Recomp's normal ROM-import process(Not tested on Yellow, so keep that in mind if you try it).
    This mod declares engine\_internals because a few compatibility and battle-animation systems hook engine modules that are not part of the stable public mod API.

This release is scoped to red in manifest.json. It is not advertised as compatible with Blue, Yellow, or Gen 2.
Installation
From a GitHub Release

    Download mars\_expanded\_kanto-1.0.0.zip from this repository's Releases page.
    Open Gen1Recomp.
    Open the Mods screen.
    Choose Import mod .zip.
    Select the downloaded archive and enable Mars's Expanded Kanto.
    Restart the game if the launcher asks you to.

The release archive is intentionally built with manifest.json, main.lua, and assets/ at the archive root.
Manual development install

Copy this repository into your Gen1Recomp mods/ directory as:

mods/
  mars\_expanded\_kanto/
    manifest.json
    main.lua
    assets/

Save-file recommendation

For a first playthrough of the public release, a new game is recommended. The mod changes world layout, encounters, progression, quests, trainer data, and postgame state extensively.

If you are upgrading an existing Expanded Kanto development save, make a backup first.
Link play

This is an overhaul and changes link-relevant Pokemon and move data, so affects\_link is true. Use the same Expanded Kanto version and compatible mod set on both peers for link features.
Compatibility

The mod was developed alongside optional mods such as Gold/Silver sprite replacements, Advanced Color, Modern Battle UI, and enhanced PC/box interfaces. They are not hard dependencies.

Because Expanded Kanto is a large overhaul, other mods that change the same maps, species, moves, encounters, battle internals, or UI hooks can still conflict. When reporting a problem, include your enabled-mod list.
Validation before release

Gen1Recomp's publishing guide requires a clean strict validation and ROM-content lint before distribution:

python3 tools/modkit.py validate /path/to/mars-expanded-kanto --strict
python3 tools/modkit.py lint /path/to/mars-expanded-kanto
python3 tools/modkit.py pack /path/to/mars-expanded-kanto -o mars\_expanded\_kanto-1.0.0.zip

Run those commands from a current Gen1Recomp source checkout. The included GitHub Actions workflow performs the same validation/packaging path for releases.
Asset distribution notice

Gen1Recomp's publishing rules prohibit shipping ROM-extracted or ROM-derived pixels. This repository contains custom and third-party-style artwork used by the mod; verify the provenance and redistribution permission of every bundled image before making the repository public. See ASSET_PROVENANCE.md and CREDITS.md.

If an image was directly extracted, recolored, or otherwise derived from an official game asset, do not publish that file. Replace it with original/authorized art or use Gen1Recomp's asset-transform workflow where applicable.
Bug reports

Please include:

    Gen1Recomp version/build
    Expanded Kanto version
    enabled mods and their versions
    what you were doing immediately before the issue
    a screenshot when useful
    the relevant game log when a crash or script error occurs

Credits

Created by MarsCrowley for the Gen1Recomp mod platform.

See CREDITS.md for engine and artwork acknowledgements.

Pokemon and related trademarks are owned by their respective rights holders. This is an unofficial fan-made mod and is not affiliated with or endorsed by Nintendo, Game Freak, Creatures, or The Pokemon Company.
