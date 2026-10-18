# Session log

Three lines per session: done, exact next step, unresolved.

## 2026-10-17
- **Done:** git repo; CMake build (C++20, warnings as errors, Debug sanitizers) with Catch2 and SDL3 via FetchContent; `mesia --smoke-test` opens a 768×720 window; Windows Debug and Release build and pass tests.
- **Next:** (license done: GPL-3.0-or-later) write the GitHub Actions workflow running `cmake --preset` / `ctest --preset` on windows-latest and ubuntu-latest.
- **Unresolved:** Linux presets untested (no Linux machine used yet; CI will be the first run). Python isn't on PATH here (only the Microsoft Store alias), and the tools need it.
