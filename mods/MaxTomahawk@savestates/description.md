# Save States

Save States adds native rolling quicksaves, event-based autosaves and permanent
save slots to Gen1Recomp without replacing the normal Pokémon save system.

This stable release requires **Gen1Recomp v0.1.80 or newer**.

## What it adds

- 50 rolling Quick Saves and 50 rolling Auto Saves by default, configurable up
  to 100 each;
- ten permanent renameable slots outside rolling retention;
- recovery before every supported load and one-level **UNDO LAST LOAD**;
- title-menu browsing and loading across a cold restart;
- **CONTINUE LATEST**, comparing normal-save and savestate capture times;
- stable overworld and deterministic supported battle decision-point restore;
- location, wild-battle and trainer-battle autosaves;
- captured location, date/time, play time, badges and full-party details;
- corruption handling, game/playthrough isolation, confirmations and native
  notifications.

Use **QUICKSAVE** or **STATES** from the in-game START menu. Use **SAVE STATES**
on the title menu to browse the selected playthrough. The ordinary Pokémon
**SAVE** command remains available and keeps its normal meaning.

If the first savestate predates the first normal Pokémon save, Gen1Recomp creates
one verified initial progress anchor so that playthrough can still be found after
a restart. Later savestates and ordinary saves remain independent.

## Autosaves and battles

Autosaves are event-driven. Location saves wait for stable overworld control;
wild and trainer battle requests wait through the intro and capture at the first
supported player decision. Optional after-battle and before-warp triggers default
to OFF.

Supported battle checkpoints include settled ordinary and validated built-in
story/trainer decisions. Gameplay RNG is restored too. Animations, messages,
forced decisions, link/Safari/ghost/demo battles, opaque scripts and other unsafe
phases are rejected instead of partially serialized.

<!-- battle-feature-note:start -->
Battle START-menu access is included in Gen1Recomp **v0.1.80 and newer** at supported decision points.
<!-- battle-feature-note:end -->

## Details and settings

<!-- icon-feature-note:start -->
Party icons in state details are included in Gen1Recomp **v0.1.80 and newer** through the public Party presentation contract.
<!-- icon-feature-note:end -->

| Setting | Default | Choices / effect |
| --- | --- | --- |
| Quick Save History | 50 | 1, 3, 5, 10, 15, 20, 30, 50, 75, 100 |
| Auto Save History | 50 | 5, 10, 20, 30, 50, 75, 100 |
| History Time | Play Time | Play Time, Date/Time, Age |
| Auto: Location Entry | On | Event autosave |
| Auto: Trainer Battle | On | First safe trainer decision |
| Auto: Wild Battle | On | First safe wild decision |
| Auto: After Battle | Off | Stable overworld return |
| Auto: Before Warp | Off | Safe pre-transition boundary |
| Save Notifications | On | Save results |
| Load Notifications | On | Load and undo results |
| Continue Latest | On | Newest valid normal save or savestate |
| Debug Timings | Off | Development performance logs |

Quick/Auto history dates are non-selectable headings. Date/time display follows
Gen1Recomp's device or chosen date/time format, with `DD-MM-YYYY` and 24-hour time
as the portable fallback.

## Safety

Snapshots are versioned data only. Gen1Recomp validates game, playthrough,
content and runtime capability before mutation, and Save States verifies durable
recovery before loading. Another mod's canonical progress rewinds with the game;
independent tool storage, current options and arbitrary runtime memory do not.

The normal Pokémon SAVE remains an independent conventional backup. The package
contains no ROM or extracted game assets.

## License

MIT
