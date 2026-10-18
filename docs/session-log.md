# Session log

Three lines per session: done, exact next step, unresolved.

## 2026-10-17
- **Done:** git repo pushed to GitHub; CMake build (C++20, warnings as errors, Debug sanitizers) with Catch2 and SDL3; GPL-3.0-or-later; GitHub Actions builds and tests Debug and Release on Windows and Linux (first run green, including the headless window smoke test).
- **Next:** add ROM blocking to `.gitignore` (`*.nes`, `*.NES`, `*.unf`, `*.fds`, extracted-data folders) and write the pre-commit hook that rejects files starting with the iNES magic bytes `NES\x1A`.
- **Unresolved:** Linux has only been built on CI, not run on a real desktop or a Steam Deck.

## 2026-10-17 (later)
- **Done:** README pushed; `rom-loader` branch created; Python tools workspace in `tools/` (pyproject with pinned pytest and ruff, venv, ignore rules). Python 3.14 was installed all along via the `py` launcher.
- **Next:** write the ROM loader on `rom-loader`: parse the 16-byte iNES header and reject anything that isn't mapper 4.
- **Unresolved:** commit `uv.lock` or not (only matters if uv becomes the standard). `CLAUDE.md` hard rules still mention a pre-commit check.
