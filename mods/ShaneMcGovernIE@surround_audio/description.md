# Stereo & 5.1 Audio

Pokemon Crystal's SOUND option, ported to the 8-bit music of Red/Blue/Yellow:

- **MONO** sums every music channel into both speakers — the straight
  Game Boy mix.
- **STEREO** splits the channels: 1-2 to the left speaker, 3-4 to the
  right, like Crystal's stereo panning. Gen 1 songs never write the pan
  register, so the split is forced at the render level.
- Every sound effect (menu beeps, battle hits, cries, fanfares, the
  low-health alarm) is positioned dead ahead of the listener — the center
  channel on a 5.1 device, the middle of the image on stereo.

Toggle with **L** (gamepad `leftshoulder`, keyboard `Q`) — the current
song restarts so the change is heard immediately — or via the **SOUND**
row in OPTIONS. The choice persists in `options.lua`.

## Install

1. Download `surround_audio-1.5.0.zip` from the
   [releases page](https://github.com/ShaneMcGovernIE/surround-audio/releases).
2. In the launcher: MODS → **Import mod .zip**.

With `"github": "ShaneMcGovernIE/surround-audio"` set, the launcher's
**Update** and **Versions** buttons handle new releases from there.
