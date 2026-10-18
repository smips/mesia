# Mesia

[![Build](https://github.com/smips/mesia/actions/workflows/build.yml/badge.svg)](https://github.com/smips/mesia/actions/workflows/build.yml)

**Mesia is an engine for playing *Crystalis* (NES, 1990) with your own ROM.**

It runs the original game code unmodified on a cycle-exact 6502 CPU and
reproduces the NES frame for frame. The picture, sound, input and saves around
it are native C++, so later versions can add features without touching the
game's own logic.

> **Status: early development.** Mesia does not play the game yet. The first
> release (v1) targets the complete original game, playable start to finish,
> matching the NES frame for frame.

## You need your own ROM

Mesia contains no game data. To play, you need a legally obtained copy of the
**US release** of *Crystalis* in iNES (`.nes`) format. Other regional releases
are not supported.

Mesia will read the ROM at runtime and check it against the known US
release. It never writes out a modified ROM; any change to how the game
behaves is made in memory while it runs.

This project does not provide ROMs and will not tell you where to find them.
Please don't ask in issues.

## How it works

- **Core (C++20):** 6502 CPU, MMC3 mapper, a dot-based PPU and the APU, all
  written from scratch for this project. Accuracy comes from emulating the
  hardware exactly, cycle by cycle, rather than imitating the game's behaviour.
- **Frontend (SDL3):** window, rendering, audio output, input and save files.
- **Tools (Python, planned):** ROM data inspection, input replay recording, and trace
  and RAM comparison against the [Mesen](https://mesen.ca/) emulator, which
  serves as the accuracy reference.

## Building

Mesia builds with CMake 3.25 or newer and a C++20 compiler. SDL3 and Catch2
are downloaded automatically at configure time, pinned to exact versions.

### Windows

Requires Visual Studio 2022 or newer with the "Desktop development with C++"
workload.

```
cmake --preset windows
cmake --build --preset windows-debug
ctest --preset windows-debug
```

Use `windows-release` for an optimized build. Executables are written to
`build/windows/bin/<Debug|Release>/`.

### Linux

Requires GCC or Clang, Ninja, and the development packages SDL3 uses. On
Ubuntu or Debian:

```
sudo apt install build-essential cmake ninja-build pkg-config \
  libx11-dev libxext-dev libxrandr-dev libxcursor-dev libxfixes-dev \
  libxi-dev libxss-dev libxtst-dev libxkbcommon-dev \
  libwayland-dev wayland-protocols libdecor-0-dev \
  libegl1-mesa-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev \
  libasound2-dev libpulse-dev libpipewire-0.3-dev \
  libudev-dev libdbus-1-dev libibus-1.0-dev
```

Then:

```
cmake --preset linux-debug
cmake --build --preset linux-debug
ctest --preset linux-debug
```

Use `linux-release` for an optimized build. Executables are written to
`build/linux-<debug|release>/bin/`.

Debug builds enable AddressSanitizer (and UndefinedBehaviorSanitizer on
GCC/Clang). Warnings are treated as errors.

## Contributing

Mesia is a solo project and isn't looking for code contributions yet, but bug
reports are welcome once it plays the game. The rules below apply to anything
in this repository:

- **No ROM data.** Never commit a ROM, a part of one, or anything extracted
  or derived from one: graphics, music, maps, text, data tables or dumps.
  Referring to ROM addresses in code and comments is fine.
- **No SNK assets.** No box art, logos, key art, screenshots of official
  material or other SNK-owned artwork, in the repository or in releases.
- **No disassembly code.** Community disassemblies of the game are useful
  references, but their code and comments must not be copied in. Anything
  that replaces game behaviour is written as original C++.

`.gitignore` blocks common ROM formats, saves and the `roms/` and
`extracted/` folders as a safety net; please don't work around it.

## License

Mesia is free software, licensed under the
[GNU General Public License v3.0 or later](LICENSE)
(`SPDX-License-Identifier: GPL-3.0-or-later`).

*Crystalis* is a trademark of SNK. Mesia is an independent project, not
affiliated with or endorsed by SNK.
