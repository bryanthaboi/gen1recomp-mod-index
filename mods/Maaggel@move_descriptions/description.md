Gen 1 never told you what a move did. You picked BODY SLAM over STOMP on a hunch, or you had the guidebook. Move descriptions arrived in Gen 2 and never left - this puts them in Gen 1.

Press START on a move and a box tells you what it does.

```
THUNDERBOLT:
> ELECTRIC  PWR 95
  ACC 100  PP 15
> May paralyze the target.
```

Name first, then the numbers, then the effect - one press each, every page sized to what the box shows without scrolling.

## Where it works

- **In battle**, on the move menu.
- **On the status screen**, page 2, walking all four moves in turn.
- **When learning a move.** The cursor's move is described, and on the CANCEL row it describes the move being *offered* - the one you actually need to judge before giving something up for it.
- **In the bag**, on a TM or HM, describing the move it teaches.
- **On the Moves Manager mod's MOVES page**, if you run it: the highlighted slot while browsing, the highlighted candidate while choosing a replacement.

## Generated, not transcribed

The text is built at runtime from the engine's own move records - `type`, `power`, `accuracy`, `pp` and `effect`. There is no table of 165 hand-written blurbs copied from a wiki.

That matters for three reasons. The numbers cannot drift from what the move actually does in this engine, because they *are* what the move does. Moves added or rebalanced by other mods get correct descriptions for free. And the descriptions describe Gen 1 behaviour rather than some later generation's wording for the same move name.

The one hand-written part is a short line per effect id - 68 of them, covering the engine's entire effect table - plus five fixed-damage moves the engine keys by move id rather than by effect, so SONICBOOM says it deals 20 and SEISMIC TOSS says it deals the user's level. Two-turn moves say so, so PWR 120 on SOLARBEAM is not mistaken for damage you get this turn.

An effect id the mod does not recognise shows the stat block with no effect line. Unknown means less information, never wrong information.

## Compatibility

Screens are detected by their own fields rather than by matching engine classes, so this keeps working if a screen is reimplemented, and does nothing at all on screens it does not recognise. No dependencies are declared.

One thing to know if you run **Modern Bag**: START in its TM/HM pocket normally opens its search hub. That hub is replaced by the description, so the TM/HM search is no longer reachable from START. Modern Bag's own move info button is unaffected and still works.

## Install

Download the release .zip and use **MODS > Import mod .zip** in the launcher, or drop the `move_descriptions` folder into your `mods/` directory. Restart afterwards - content registries freeze at boot.

## Credits

By Maaggel. MIT licensed. Source and releases: https://github.com/Maaggel/move-descriptions

No ROM-derived content. Lua and text only.
