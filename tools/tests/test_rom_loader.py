# SPDX-License-Identifier: GPL-3.0-or-later

# Tests for rom_loader.py. They build synthetic ROM images in memory, so no
# real ROM (or anything derived from one) is ever needed or committed.

from rom_loader import (
    CHR_OUTPUT_FILE,
    FILE_EXPECTED_CHR_SIZE,
    FILE_EXPECTED_PRG_SIZE,
    PRG_OUTPUT_FILE,
    ROM,
    extract_rom_data,
)


def make_header(
    prg_banks: int = 16,
    chr_banks: int = 16,
    mapper: int = 4,
    flags6_low: int = 0x00,
) -> bytes:
    """Build a 16-byte iNES header. The defaults describe a Crystalis-shaped ROM."""
    flags6 = ((mapper & 0x0F) << 4) | (flags6_low & 0x0F)
    flags7 = mapper & 0xF0
    return b"NES\x1a" + bytes([prg_banks, chr_banks, flags6, flags7]) + bytes(8)


def test_valid_header_loads_prg_and_chr():
    prg = b"\x11" * FILE_EXPECTED_PRG_SIZE
    chr_data = b"\x22" * FILE_EXPECTED_CHR_SIZE

    rom = ROM(make_header() + prg + chr_data)

    assert rom.header.mapper == 4
    assert rom.prg == prg
    assert rom.chr == chr_data


def test_extract_rom_data(tmp_path):
    prg = b"\x11" * FILE_EXPECTED_PRG_SIZE
    chr_data = b"\x22" * FILE_EXPECTED_CHR_SIZE

    rom = ROM(make_header() + prg + chr_data)

    out_dir = tmp_path / "extracted"
    extract_rom_data(rom, out_dir)

    prg_file = out_dir / PRG_OUTPUT_FILE
    chr_file = out_dir / CHR_OUTPUT_FILE

    assert prg_file.exists()
    assert chr_file.exists()

    assert prg_file.read_bytes() == prg
    assert chr_file.read_bytes() == chr_data
    assert sorted(p.name for p in out_dir.iterdir()) == sorted([CHR_OUTPUT_FILE, PRG_OUTPUT_FILE])
