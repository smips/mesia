# Session log

Three sections per session: done, exact next step, unresolved. One bullet per item.

## 2026-10-17

**Done**
- Git repo pushed to GitHub
- CMake build (C++20, warnings as errors, Debug sanitizers) with Catch2 and SDL3
- License: GPL-3.0-or-later
- GitHub Actions builds and tests Debug and Release on Windows and Linux (first run green, including the headless window smoke test)

**Next**
- Add ROM blocking to `.gitignore` (`*.nes`, `*.NES`, `*.unf`, `*.fds`, extracted-data folders)
- Write the pre-commit hook that rejects files starting with the iNES magic bytes `NES\x1A`

**Unresolved**
- Linux has only been built on CI, not run on a real desktop or a Steam Deck

## 2026-10-17 (later)

**Done**
- README pushed
- `rom-loader` branch created
- Python tools workspace in `tools/` (pyproject with pinned pytest and ruff, venv, ignore rules)
- Python 3.14 was installed all along via the `py` launcher

**Next**
- Write the ROM loader on `rom-loader`: parse the 16-byte iNES header and reject anything that isn't mapper 4

**Unresolved**
- Commit `uv.lock` or not (only matters if uv becomes the standard)
- `CLAUDE.md` hard rules still mention a pre-commit check

## 2026-10-17 (evening, rom_loader.py)

**Done**
- `tools/rom_loader.py` (uncommitted): lists `roms/` with a `pick` menu, checks file size (393,232 bytes = 16-byte header + 256 KiB PRG + 128 KiB CHR, correct), SHA-1 and CRC32
- Header parsing is a `NotImplementedError` stub
- Size check passes on the US ROM; both hash checks fail

**Next**
- Fix the hash checks: compare case-insensitively (`hexdigest()` and `:08x` give lowercase, the constants are uppercase)
- Re-source the expected values from a verified US dump listing, hashing PRG+CHR without the header as the plan says
  - The file currently hashes to whole-file SHA-1 `c9144b47…` / CRC32 `f8f1865d`, headerless `8a49fe60…` / `1335cb05`
  - Neither matches `FD0DCDE4…` / `1BD39032` in any case

**Unresolved**
- `pick` isn't listed in `pyproject.toml` dependencies
- `ROM_PATH = "..\roms"` depends on the working directory and breaks on Linux (build it from `__file__` with `pathlib`)
- The file is read twice
- No tests yet
- Decide whether this Python loader is a prototype for the C++ core loader (week 1 item) or a separate tool

## 2026-10-19 (rom_loader.py audit)

**Done**
- `rom_loader.py` now has `iNesHeader`/`ROM` classes, slices PRG and CHR, hashes PRG+CHR, and checks the header magic and exact header bytes
- Hash comparisons are now case-consistent
- Audited it (19 findings, file unchanged by the audit). Blocking bugs:
  1. `check_rom_header_values` compares the header object to `bytes`, so it always fails; even `header.data` wouldn't match, because the US ROM has an NES 2.0 header (bytes 7=`0x08`, 10=`0x70`, 15=`0x01`)
  2. The expected hashes were copied from this same file, so they prove nothing
  3. Whole-file hashes reject correct dumps with other headers
  4. The header is validated last, and sizes come from constants rather than the header

**Next**
- Replace `check_rom_header_values` with a decoded-field check, run before any slicing:
  - magic `NES\x1A`
  - mapper `(flags6 >> 4) | (flags7 & 0xF0) == 4`
  - PRG `data[4] * 16384 == 262144`
  - CHR `data[5] * 8192 == 131072`

**Unresolved**
- Source the PRG+CHR hashes from an independent verified listing (No-Intro or Data Crystal)
- Remaining cleanup from the audit:
  - exit code 1 on failure
  - read the file once
  - keep printing out of the `check_*` functions
  - `ROM_PATH` from `__file__`
  - CLI path argument with `pick` as fallback
  - add `pick` to `pyproject.toml`
  - simplify the CRC formatting
  - colour helpers
  - pytest tests on synthetic headers
  - 24 ruff errors
  - PEP 8 class names

## 2026-10-21 (rom_loader.py cleanup, first test)

**Done**
- Worked through four audit passes on `rom_loader.py`. It now:
  - checks the iNES magic, then Crystalis shape (mapper 4, 256 KiB PRG, 128 KiB CHR) from decoded header fields
  - skips a trainer (flags 6 bit 2)
  - requires the exact file size
  - hashes PRG+CHR
  - reports errors through `print_fail`/`print_success` and exits 1 on failure
- ruff check and format are clean
- `pick==2.6.0` is a runtime dependency
- Added `tools/tests/test_rom_loader.py` with a `make_header()` helper and one passing example test (`pythonpath = ["."]` added to the pytest settings)

**Next**
- Write the remaining tests in `test_rom_loader.py`: mirroring bit, trainer, trailing byte, wrong magic, wrong mapper, wrong PRG/CHR size
- Then make `rom_loader.py` write the PRG and CHR data to disk, only under the git-ignored `/extracted/` folder

**Unresolved**
- Couldn't verify the expected Crystalis hashes (`8A49FE60…` / `1335CB05`) because the reference websites were down for unplanned maintenance, so they still come from the local file
- Still open from the audit:
  - `ROM_PATH` depends on the working directory and uses a Windows backslash
  - the picker is interactive only and lists every file in `roms/`
  - "DiskDude!" headers are rejected

## 2026-10-25 (rom_loader.py extraction)

**Done**
- `rom_loader.py` writes PRG and CHR to `extracted/prg.bin` and `extracted/chr.bin` after validation, through `write_binary_file` (temp file + `os.replace`, temp file removed on failure)
- `ROM_PATH`/`EXTRACT_PATH` are now built from `__file__`, so output always lands in the git-ignored root `/extracted/` on any OS and from any working directory
- Added `print_info` and tidied terminal output
- Four audit passes; ruff clean, 1 test passing
- Committed and pushed as `f08f671`

**Next**
- Move the extraction in `main()` into `extract(rom, out_dir)` and add a pytest that calls it with `tmp_path` and checks both files byte for byte
- Then write the seven header/size tests: mirroring bit, trainer, trailing byte, wrong magic, wrong mapper, wrong PRG size, wrong CHR size

**Unresolved**
- Expected hashes still come from the local file (verify against No-Intro or Data Crystal)
- `rom_loader.py` has CRLF line endings (consider a `.gitattributes`)
- Still no pre-commit hook
- Picker is interactive only and lists every file in `roms/`
- "DiskDude!" headers are rejected

## 2026-10-25 (later, extraction refactor and test)

**Done**
- Moved extraction into `extract_rom_data(rom, extract_path)`, which creates the folder and writes `PRG_OUTPUT_FILE`/`CHR_OUTPUT_FILE` (temp files now `<name>.tmp`); committed as `6c07c62`
- Added `test_extract_rom_data`, which checks both files byte for byte in `tmp_path` and that no temp file is left
- ruff clean, 2 tests passing

**Next**
- In `tools/tests/test_rom_loader.py`, write `test_wrong_magic_is_rejected` using `make_header()` with the first 4 bytes replaced and `pytest.raises(ValueError)`
- Then the other six header/size tests: mirroring bit, trainer, trailing byte, wrong mapper, wrong PRG size, wrong CHR size

**Unresolved**
- Expected hashes still come from the local file (verify against No-Intro or Data Crystal)
- `rom_loader.py` has CRLF line endings (consider a `.gitattributes`)
- No pre-commit hook yet
- Picker is interactive only and lists every file in `roms/`
- "DiskDude!" headers are rejected

## 2026-10-29 (header tests, hash verification, line endings)

**Done**
- `test_rom_loader.py` covers all seven header/size cases plus the NES 2.0 marker: 10 tests passing; rejection tests pin their exact error with `match=`, and wrong-size tests use data that matches the header
- `make_header()` gained `magic` and `flags7_low`
- Verified the headerless PRG+CHR SHA-1 `8A49FE60…` and CRC32 `1335CB05` against No-Intro: they match the local ROM and `rom_loader.py`
- Fixed the CRLF warning: only the working copy of `rom_loader.py` was CRLF; the repo was already LF via `.gitattributes`
- Added `.editorconfig`: LF, UTF-8, final newline, trim whitespace, 4-space indent, 2 for YAML/JSON
- Pinned Mesen 2.2.1 as the reference emulator; version and SHA-256 recorded in `docs/decisions.md`
- Saved the shared trace format to `tools/mesen/trace-format.txt`: PC, opcode bytes, A, X, Y, P, SP, CPU cycle count, scanline, dot, frame, then disassembly last

**Next**
- Power on Crystalis in Mesen 2.2.1 with the trace logger set to `tools/mesen/trace-format.txt` and log the first frame to `extracted/` (traces contain ROM bytes)
- Record the first `CYC` value and the pre-render `SL` value (-1 or 261) in `docs/decisions.md`

**Unresolved**
- The ROM picker is interactive only and lists every file in `roms/`
- "DiskDude!" headers are rejected
- VS Code needs the EditorConfig extension to apply `.editorconfig`
- Commit `3a4e5c2` (pushed) still contains the maintainer's first name in the session log, so removing it needs a history rewrite and force-push

## 2026-11-19 (power-on alignment, week 2 plan, core stubs)

**Done**
- Traced frames 1 and 2 in Mesen 2.2.1 and recorded in `docs/decisions.md`:
  - first instruction at CYC 8, SL 0, dot 27 (dot = 3 × CYC + 3)
  - FR starts at 1 and goes up at SL 240, dot 0
  - pre-render line is -1
- Dropped `[PC,4h]` from `tools/mesen/trace-format.txt`: Mesen always adds the PC prefix, so Mesia's tracer must print it itself
- Decided the C++ core loads `extracted/prg.bin`/`chr.bin`, and that the cartridge holds only fixed data while a separate plain `Mmc3` class owns mapper state
- Checked off week 1 and wrote the week 2 task list (gate: Mesia's frame 1 trace matches `extracted/Crystalis_frame1.txt`)
- Added empty `cartridge` and `mmc3` stubs to `mesia_core`; Windows Debug and Release build and test clean

**Next**
- In `cartridge.hpp`, declare the cartridge class with PRG and CHR byte storage and a load function that takes the folder holding `prg.bin` and `chr.bin`
- Then write the first Catch2 test in `tests/cartridge_test.cpp` that loads synthetic 256 KiB/128 KiB files from a temp folder and checks the bytes

**Unresolved**
- The stubs haven't been built on Linux outside CI
- The ROM picker is interactive only and lists every file in `roms/`
- "DiskDude!" headers are rejected
- Commit `3a4e5c2` still contains a name in its history (removing it needs a history rewrite and force-push)

## 2026-11-21 (cartridge class draft, exceptions library, test layout)

**Done**
- Declared `mesia::Cartridge` in `cartridge.hpp` with `load(filename)` (throws the new `NotImplementedException`) and bounds-checked `read_prg`/`read_chr`
- Added a header-only `src/exceptions` library (`mesia/not_implemented.hpp`) behind a new `MESIA_BUILD_EXCEPTIONS` option, included by `mesia_core`
- The root `CMakeLists.txt` gained `include(FetchContent)`. Catch2, Boost and SDL3 declarations were drafted there but removed before commit, though the commit message for `9f4fd8d` still mentions them
- Chose a test layout: one `mesia_tests` executable, `tests/core/` mirroring `src/core/`, shared helpers (a `TempDir` RAII folder) in `tests/support/`

**Next**
- Change `_prg`/`_chr` in `cartridge.hpp` to `std::vector<std::uint8_t>` sized 256 KiB/128 KiB
- Then create `tests/support/temp_dir.hpp` and a failing `tests/core/cartridge_test.cpp` that writes synthetic `prg.bin`/`chr.bin` with an offset pattern and checks the first and last byte of each, and add both to `tests/CMakeLists.txt`

**Unresolved**
- Whether to keep Boost (C++20 `std::filesystem` covers the current need; decide and record in `docs/decisions.md`)
- `load` should take the folder and report errors clearly (exception with file name and expected size, not `bool`)
- `not_implemented.hpp` lacks `#pragma once`, and `cartridge.cpp` lacks `<algorithm>`
- Untracked `libs/` holds leftover submodule stubs and is not committed

## 2026-11-22 (cartridge storage and errors, test folders)

**Done**
- Moved `NotImplementedException` into the core as `mesia/exceptions.hpp` and deleted the `src/exceptions` library
- Added `CartridgeError` (a `std::runtime_error`) to `cartridge.hpp`
- PRG/CHR storage is now `std::vector<uint8_t>` sized 256 KiB/128 KiB
- `load` checks that `prg.bin`/`chr.bin` exist with the right sizes, then still throws `NotImplementedException`
- Added `tests/support/temp_dir.hpp` (`TempDir`) and `tests/core/cartridge_test.cpp` (instantiation test), wired into `tests/CMakeLists.txt`
- Settled:
  - one `mesia_tests` executable with sources listed by path (no per-folder test libraries, since the linker drops unreferenced Catch2 test objects from static libraries)
  - `std::uint8_t` for bytes
  - `load` throws only `CartridgeError`, using the `std::error_code` filesystem overloads so filesystem errors don't escape as their own type
- Fixed `TempDir`: a single `append` of `"mesia_test_" + number` (the old leading `/` sent the path to the drive root, and the second `append` added a separate folder level)
- Fixed `read_prg`/`read_chr`: `.size()` instead of `sizeof`
- Windows Debug builds clean, 3 tests pass

**Next**
- Add a test in `cartridge_test.cpp` that writes 256 KiB `prg.bin` and 128 KiB `chr.bin` filled with `(i ^ (i >> 8)) & 0xFF` into a `TempDir`, calls `load`, and checks the first and last byte of each

**Unresolved**
- `read_prg`/`read_chr` take the offset as `unsigned short`, which only reaches the first 64 KiB, so most of PRG (256 KiB) and half of CHR (128 KiB) are unreachable: use `std::uint32_t` (the `Mmc3` class will pass full cartridge offsets)
- `load` builds paths from `parent_path()` of its argument, but the task says the caller passes the folder itself
- `load` still returns `bool` and should throw `CartridgeError` with the file name and expected size
- `cartridge.hpp` uses `std::runtime_error` without `#include <stdexcept>`
- The unused `MESIA_BUILD_EXCEPTIONS` option is still in the root `CMakeLists.txt`
- `tests/version_test.cpp` hasn't moved to `tests/core/`
- Boost decision still open (record in `docs/decisions.md`)
- Untracked `libs/` holds leftover submodule stubs and is not committed
- Add build and test scripts (PowerShell on Windows, shell on Linux) that configure, build and run ctest for every configuration through the `CMakePresets.json` presets, possibly as CMake workflow presets
- Not built on Linux outside CI

## 2026-11-22 (later, cartridge load)

**Done**
- `Cartridge::load` now takes the data folder, checks that `prg.bin` and `chr.bin` exist with sizes 256 KiB and 128 KiB, reads both, and throws `CartridgeError` on any failure (returns `void`)
- `read_prg`/`read_chr` take a `uint32_t` offset, so the whole of PRG and CHR is reachable
- `cartridge.hpp` includes `<stdexcept>`
- Removed the `MESIA_BUILD_EXCEPTIONS` option
- Moved `version_test.cpp` to `tests/core/`
- New test `Cartridge class can load PRG and CHR data` writes synthetic files with the `(i ^ (i >> 8)) & 0xFF` pattern into a `TempDir`, loads them, and checks the first and last byte of each plus the out-of-range reads
- Windows Debug builds clean, 4 tests pass

**Next**
- Fix the two Linux CI breaks:
  - in `cartridge.cpp`, pass `static_cast<std::streamsize>(_prg.size())` (and the same for `_chr`) to `read` (GCC `-Wsign-conversion` fails the build, checked locally with g++)
  - in `cartridge_test.cpp`, build paths with `std::filesystem::path` and `/` instead of `+ "\..."` (on Linux the backslash becomes part of the folder name, `load` finds nothing, and the folder is left in `/tmp` outside the `TempDir`)
- Then add `CartridgeError` tests for missing `prg.bin`, missing `chr.bin`, and each file one byte short and one byte long

**Unresolved**
- Error messages don't name the file path or the expected and actual sizes
- `load` uses the throwing `file_size` overloads rather than the `std::error_code` ones, so a permissions error would still escape as `filesystem_error`
- The load test prints its path with `std::cout`
- `cartridge.cpp` still includes the unused `mesia/exceptions.hpp`
- Stray `;` after the namespace in `cartridge_test.cpp` and `temp_dir.hpp` (harmless)
- Boost decision still open (record in `docs/decisions.md`)
- Untracked `libs/` holds leftover submodule stubs and is not committed
- Add build and test scripts for every configuration through the `CMakePresets.json` presets, possibly as CMake workflow presets

## 2026-11-22 (later, cartridge error handling and tests)

**Done**
- Fixed both Linux CI breaks: `static_cast<std::streamsize>` for the reads; test paths built with `std::filesystem::path`
- `load` uses the `std::error_code` overloads of `exists` and `file_size`, checking `ec` before the result
- Every `CartridgeError` names the file path; size errors give expected and actual sizes
- Removed the unused `mesia/exceptions.hpp` include, the test's `std::cout` and the stray `;` after namespaces
- `cartridge_test.cpp` is complete for now:
  - load and read-back
  - missing `prg.bin`, missing `chr.bin`
  - each file one byte short and one byte long
  - each case in its own `SECTION` (fresh `TempDir`), checked with `REQUIRE_THROWS_MATCHES` on type and message
  - `create_test_data` `REQUIRE`s that each file opens
- Windows Debug builds clean, 6 tests pass (30 cartridge assertions); g++ with the CI warning flags compiles both files clean
- Ticked the cartridge task in `CLAUDE.md`, recorded the no-Boost decision in `docs/decisions.md`, and deleted the leftover `libs/` folder
- Reformatted this log: three sections per entry, one bullet per item

**Next**
- In `mmc3.hpp`, declare `Mmc3` holding a `const Cartridge&` with `uint8_t cpu_read(uint16_t address) const`, mapping `$C000`–`$DFFF` to cartridge offset `0x3C000 + (address - 0xC000)` and `$E000`–`$FFFF` to `0x3E000 + (address - 0xE000)`
- Then write `tests/core/mmc3_test.cpp` checking `$C000`, `$DFFF`, `$E000` and `$FFFF` against those offsets with the synthetic-pattern files, and add it to `tests/CMakeLists.txt`

**Unresolved**
- If the CHR read fails after the PRG read succeeds, `_prg` is already overwritten (harmless while a failed load is fatal)
- Add build and test scripts for every configuration through the `CMakePresets.json` presets, possibly as CMake workflow presets
- Linux build of these changes only confirmed once CI runs

## 2026-11-23 (MMC3 registers)

**Done**
- Decided on the `Mmc3` structure: register state grouped in plain structs by function (`BankControl` for `$8000`/`$8001`, `Irq` for `$C000`–`$E001`), with mirroring and PRG RAM flags as members; all logic stays in `Mmc3`
- Decided to bring bank select forward from week 3: frame 1 only stores to `$2000` and `$2001`, so the gate doesn't exercise it, but it's small and self-contained
- Testing plan: test `Mmc3` on its own through `write`, `read_prg` and `read_chr`, using synthetic PRG/CHR files whose bytes identify their bank and offset (runs on CI; real-ROM checks could be an optional `[rom]` suite later)
- `Mmc3` declared with a `const Cartridge&` constructor, `write`, `read_prg` and `read_chr`
- `write` decodes the register with `address & 0xE001` and stores all eight registers (bank select, bank data, mirroring, PRG RAM protect, IRQ latch, reload, disable, enable); writes take effect immediately
- `read_prg` and `read_chr` throw `NotImplementedException`, which now takes the function name for its message
- Added an empty `tests/core/mmc3_test.cpp` to `tests/CMakeLists.txt`
- Windows Debug builds clean; the 6 existing tests pass

**Next**
- In `tests/core/mmc3_test.cpp`, write a helper that creates synthetic `prg.bin` (32 × 8 KiB) and `chr.bin` (128 × 1 KiB) in a `TempDir`, with byte 0 of each bank set to its bank number and the rest set to `bank ^ (offset & 0xFF)`, then write a failing test that power-on `read_prg(0xE000)` returns 31 and `read_prg(0xC000)` returns 30
- Then implement `read_prg`: precompute four 8 KiB bank offsets on every `$8000`/`$8001` write (R6/R7 masked with `0x1F`; PRG mode swaps `$8000` and `$C000`), and add tests for R6/R7 switching, PRG mode 1 and out-of-range bank wrap

**Unresolved**
- `$A000` mirroring is inverted: `horizontalMirroring = (value & 0x01) == 0` should be `!= 0` (bit 0 set means horizontal)
- `read_chr` parameter is named `cpu_address` but takes a PPU address (`$0000`–`$1FFF`)
- `exceptions.hpp` uses `std::string` without including `<string>` (compiles through `<stdexcept>` today)
- `mmc3_test.cpp` has no SPDX header yet
- R0/R1 must ignore their low bit (2 KiB CHR banks), and R6/R7 their top two bits, when bank offsets are computed
- PRG RAM at `$6000`–`$7FFF` and open bus for a disabled PRG RAM are not handled (not needed until the game uses them)
- Add build and test scripts for every configuration through the `CMakePresets.json` presets, possibly as CMake workflow presets
