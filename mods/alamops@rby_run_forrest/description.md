# Run Forrest

Hold **B** and two things happen: you run at bike speed, and every ledge in the
game becomes two-way.

Both generations ship the same one-way shortcut and neither ships the way back.
You drop off the ledge outside Mt. Moon, realise the item you wanted was on the
plateau, and walk the long way round. This gives you the short way back — but
only while you are asking for it. Let go of B and every ledge is exactly the
one-way shortcut its designers drew.

![Climbing a Route 4 ledge: below it, mid-air, on top](https://raw.githubusercontent.com/alamops/RBYRunForrest/main/docs/images/gen1-climb-2-midair.png)

## What you get

- **Running.** A tile takes half as long on foot — the Gen 3+ Running Shoes
  figure. The arithmetic divides whatever walk speed the engine hands over, so a
  data pack that says a tile is 24 frames gets a 12-frame run rather than being
  quietly slowed to the vanilla 8.
- **Climbing.** Press back into a ledge with B held and you hop up it. South
  ledges climb with UP, west ledges with RIGHT, east ledges with LEFT — every
  one-way hop reversed, in the direction it came from.
- **On the bike too.** B gates the climb on foot and mounted alike. It cannot
  collide with Cycling Road's held-B brake, which is the branch the engine takes
  when *no* direction is held.
- **In stride.** Run at a ledge and you climb it without stopping — no pause, no
  second press, the same way vanilla hops one the moment you walk into it from
  the top.

## What it refuses

A mountain-wall face is not a ledge and never becomes one. Neither is a cell you
could simply have walked into: if the gap in front of you is open ground you
walk it, because a two-cell jump across open ground is a teleport, not a climb.
Blocked or occupied landings, the edge of the map, and surfing are all refused.

Two toggles under **START → OPTIONS**, both on by default and independent:
`B TO RUN` and `B TO CLIMB`.

## How it works

One geometric rule serves both games:

> a hop from A over B onto C means a climb from C over B onto A

What differs is where each game writes the ledge down. Gen 1 marks the cliff
face *between* and names it in a `data.field.ledges` row; Gold marks the *far
side*, whose tile is walkable land with a wall in front of it. So the Gen 1 arm
reads one cell ahead and the Gold arm reads two, and both then ask the same two
questions: is the gap refused, is the landing free.

No vanilla path is patched out. The climb is decided on `input.step`, before the
pad's edges are promoted, so the engine's own `if player.moving then return`
stands down of its own accord. Each generation's climb is executed by mirroring
that generation's own forward hop, which is why the arc and the hop shadow are
the game's own and it looks like the drop played backwards.

## Compatibility

Red, Blue, Yellow and Gold. Works offline — it is a movement feature that
happens to be dual-generation, not a connection feature. `affects_link` is
false; no link-surface data is touched.

**Known limitation:** Yellow's Pikachu does not arc with you on a climb. The
follower recognises a ledge by matching the forward row inside a local the mod
cannot reach, so it walks to the cell you took off from and follows a step
later. It self-corrects and never gets stuck.

## Verification

136 checks across four suites, all green on the released code: a headless suite
on both generations driving the real loader and a real Gold `World`; live runs
in the game on real Route 4 and Route 29 map data, including mid-air captures of
every climb; and the engine's own ledge regression driver re-run with this mod
loaded, to show vanilla ledge behaviour is unchanged.
