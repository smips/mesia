# Mesia tools

Python development tools for Mesia. None of them ship with the engine.

Planned:

- **ROM data dumper:** inspect data tables in the player's ROM. Output goes
  to `/extracted/`, which git ignores; never commit it.
- **Input replay recorder:** record controller input per frame so the same
  run can be played back in Mesia and Mesen.
- **Trace and RAM diff:** compare CPU traces and per-frame RAM dumps against
  Mesen and report the first divergence.

## Setup

Requires Python 3.12 or newer. From this folder:

```
# Windows
py -3 -m venv .venv
.venv\Scripts\activate

# Linux
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install --group dev
```

`--group` needs pip 25.1 or newer, hence the upgrade. With
[uv](https://docs.astral.sh/uv/), `uv sync` does the same in one step.

## Checks

```
ruff check .
ruff format --check .
pytest
```

Tests go in `tests/`; pytest finds them there automatically.
