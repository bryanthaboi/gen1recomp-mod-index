# Voxel Ascendant

Voxel Ascendant renders the Gen1Recomp overworld as a depth-tested voxel
diorama and can stage battles in 3D using the game's existing Gen 1 battle art.
It is a standalone graphics mod; Kanto Ascendant is supported as an optional
companion but is not required.

## Features

- voxel overworld with curated, orbit, first-person and collision-aware
  third-person camera modes
- native Gen 1 battle cards staged on nearby voxel terrain or procedural discs
- optional shadows, voxel seams, supersampling and tilt-shift blur
- deterministic day, night, dusk, dawn and cycling light
- curved horizon and configurable voxel water/reflections
- controller, mouse, keyboard and open-screen touch camera input
- graceful fallback to Gen1Recomp's normal 2D renderer when a graphics feature
  is unavailable
- a documented public wall-decal API for compatible companion mods

The release intentionally includes no Pokémon or trainer art collection. It
uses images already supplied by the game or by another compatible content mod.

## Installation

Requires Gen1Recomp 0.1.90 or newer and a graphics driver with shader and
depth-canvas support. Install `VOXEL_ASCENDANT-<version>.zip` through the mod
manager. Use **Check for updates** for later releases.

## Compatibility

Voxel Ascendant owns the voxel render pipeline and therefore conflicts with
Dramatic Shape, Dramaless Shape, Battle Art Voxel Fork, PotatoVoxel and
Terrarium. Enable only one renderer at a time. It does not change link-relevant
gameplay data.

## License and provenance

Voxel Ascendant is MIT licensed and derived from the MIT-licensed
DramaticShapeVoxelMod v1.6.1 source. The repository preserves the original
license and documents the exact fork history, third-party notices and credits.
