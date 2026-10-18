# Decisions

One line each, with the reason. Newest at the bottom.

- 2026-10-17 — Dependencies come from CMake FetchContent pinned to exact tags (SDL release-3.4.18, Catch2 v3.16.1): same versions on Windows and Linux with no package manager to install.
- 2026-10-17 — SDL3 is built as a shared library: avoids static C++/ASan mismatch issues and matches how Linux distributions ship it.
- 2026-10-17 — Windows builds use MSVC through the "Visual Studio 18 2026" generator (multi-config); Linux uses Ninja with separate Debug and Release presets: each is the native toolchain on its platform.
- 2026-10-17 — Debug sanitizers: ASan+UBSan on GCC/Clang, ASan only on MSVC (all it supports). Applied globally so dependencies are instrumented the same way; MSVC will not link mixed ASan/non-ASan C++ code.
- 2026-10-17 — Warnings-as-errors applies only to Mesia's own targets, not fetched dependencies: we can't fix warnings in third-party code.
- 2026-10-17 — All binaries and DLLs go to `build/<preset>/bin/<config>`: SDL3.dll and the ASan runtime are found without PATH changes.
- 2026-10-17 — License: GPL-3.0-or-later (full text in `LICENSE`, from gnu.org): maintainer's choice; copyleft keeps the engine and any forks open, in line with "free and open source".
- 2026-10-17 — Every C++ and CMake source file starts with `SPDX-License-Identifier: GPL-3.0-or-later`: the license is machine-readable per file and survives files being copied out of the repo.
- 2026-10-17 — CI is GitHub Actions: Windows (windows-latest, MSVC) and Linux (Ubuntu 24.04, GCC), Debug and Release each, running every ctest test: the repo is on GitHub and its runners are free for public repos.
- 2026-10-17 — The Windows preset doesn't name a Visual Studio version; CMake picks the newest installed: works locally on VS 2026 and on CI runners whatever VS they ship.
- 2026-10-17 — The frontend smoke test runs under ctest with `SDL_VIDEO_DRIVER=dummy`: CI machines have no display.
- 2026-10-17 — `.gitattributes` forces LF line endings: identical files on Windows and Linux.
- 2026-10-17 — `.gitignore` blocks ROM formats (.nes, .unf/.unif, .fds, .nsf/.nsfe, .prg, .chr), `/roms/`, `/extracted/`, battery saves and Mesen save states, matching any letter case: a backstop for the "no ROM-derived data" rule on case-sensitive filesystems.
