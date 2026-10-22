# SPDX-License-Identifier: GPL-3.0-or-later

# Tests for rom_loader.py. They build synthetic ROM images in memory, so no
# real ROM (or anything derived from one) is ever needed or committed.

from rom_loader import (
    FILE_EXPECTED_CHR_SIZE,
    FILE_EXPECTED_PRG_SIZE,
    ROM,
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
