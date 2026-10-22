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

## 2026-10-17 (evening, rom_loader.py)
- **Done:** `tools/rom_loader.py` (uncommitted): lists `roms/` with a `pick` menu, checks file size (393,232 bytes = 16-byte header + 256 KiB PRG + 128 KiB CHR, correct), SHA-1 and CRC32; header parsing is a `NotImplementedError` stub. Size check passes on the US ROM; both hash checks fail.
- **Next:** fix the hash checks: compare case-insensitively (`hexdigest()` and `:08x` give lowercase, the constants are uppercase), then re-source the expected values from a verified US dump listing, hashing PRG+CHR without the header as the plan says (the file currently hashes to whole-file SHA-1 `c9144b47…` / CRC32 `f8f1865d`, headerless `8a49fe60…` / `1335cb05`; neither matches `FD0DCDE4…` / `1BD39032` in any case).
- **Unresolved:** `pick` isn't listed in `pyproject.toml` dependencies; `ROM_PATH = "..\roms"` depends on the working directory and breaks on Linux (build it from `__file__` with `pathlib`); the file is read twice; no tests yet. Also decide whether this Python loader is a prototype for the C++ core loader (week 1 item) or a separate tool.

## 2026-10-19 (rom_loader.py audit)
- **Done:** `rom_loader.py` now has `iNesHeader`/`ROM` classes, slices PRG and CHR, hashes PRG+CHR, and checks the header magic and exact header bytes. Hash comparisons are now case-consistent. Audited it (19 findings, file unchanged by the audit). Blocking bugs: (1) `check_rom_header_values` compares the header object to `bytes`, so it always fails; even `header.data` wouldn't match, because the US ROM has an NES 2.0 header (bytes 7=`0x08`, 10=`0x70`, 15=`0x01`); (2) the expected hashes were copied from this same file, so they prove nothing; (3) whole-file hashes reject correct dumps with other headers; (4) the header is validated last and sizes come from constants rather than the header.
- **Next:** replace `check_rom_header_values` with a decoded-field check: magic `NES\x1A`, mapper `(flags6 >> 4) | (flags7 & 0xF0) == 4`, PRG `data[4] * 16384 == 262144`, CHR `data[5] * 8192 == 131072`; run it before any slicing.
- **Unresolved:** source the PRG+CHR hashes from an independent verified listing (No-Intro or Data Crystal). Remaining cleanup from the audit: exit code 1 on failure, read the file once, keep printing out of the `check_*` functions, `ROM_PATH` from `__file__`, CLI path argument with `pick` as fallback, add `pick` to `pyproject.toml`, simplify the CRC formatting, colour helpers, pytest tests on synthetic headers, 24 ruff errors, PEP 8 class names.

## 2026-10-21 (rom_loader.py cleanup, first test)
- **Done:** worked through four audit passes on `rom_loader.py`. It now checks the iNES magic, then Crystalis shape (mapper 4, 256 KiB PRG, 128 KiB CHR) from decoded header fields; skips a trainer (flags 6 bit 2); requires the exact file size; hashes PRG+CHR; reports errors through `print_fail`/`print_success` and exits 1 on failure; ruff check and format are clean. `pick==2.6.0` is a runtime dependency. Added `tools/tests/test_rom_loader.py` with a `make_header()` helper and one passing example test (`pythonpath = ["."]` added to the pytest settings).
- **Next:** write the remaining tests in `test_rom_loader.py` (mirroring bit, trainer, trailing byte, wrong magic, wrong mapper, wrong PRG/CHR size), then make `rom_loader.py` write the PRG and CHR data to disk, only under the git-ignored `/extracted/` folder.
- **Unresolved:** couldn't verify the expected Crystalis hashes (`8A49FE60…` / `1335CB05`) because the reference websites were down for unplanned maintenance, so they still come from the local file. Still open from the audit: `ROM_PATH` depends on the working directory and uses a Windows backslash; the picker is interactive only and lists every file in `roms/`; "DiskDude!" headers are rejected.
