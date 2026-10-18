# Session log

Three lines per session: done, exact next step, unresolved.

## 2026-10-17
- **Done:** git repo pushed to GitHub; CMake build (C++20, warnings as errors, Debug sanitizers) with Catch2 and SDL3; GPL-3.0-or-later; GitHub Actions builds and tests Debug and Release on Windows and Linux (first run green, including the headless window smoke test).
- **Next:** add ROM blocking to `.gitignore` (`*.nes`, `*.NES`, `*.unf`, `*.fds`, extracted-data folders) and write the pre-commit hook that rejects files starting with the iNES magic bytes `NES\x1A`.
- **Unresolved:** Python isn't on PATH here (only the Microsoft Store alias), and the tools need it. Linux has only been built on CI, not run on a real desktop or a Steam Deck.
