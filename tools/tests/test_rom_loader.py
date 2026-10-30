# SPDX-License-Identifier: GPL-3.0-or-later

# Tests for rom_loader.py. They build synthetic ROM images in memory, so no
# real ROM (or anything derived from one) is ever needed or committed.

import pytest

from rom_loader import (
    CHR_OUTPUT_FILE,
    FILE_EXPECTED_CHR_SIZE,
    FILE_EXPECTED_PRG_SIZE,
    HEADER_CHR_BANK_SIZE,
    HEADER_PRG_BANK_SIZE,
    PRG_OUTPUT_FILE,
    ROM,
    extract_rom_data,
)


def make_header(
    magic: bytes = b"NES\x1a",
    prg_banks: int = 16,
    chr_banks: int = 16,
    mapper: int = 4,
    flags6_low: int = 0x00,
    flags7_low: int = 0x00,
) -> bytes:
    """Build a 16-byte iNES header. The defaults describe a Crystalis-shaped ROM."""
    flags6 = ((mapper & 0x0F) << 4) | (flags6_low & 0x0F)
    flags7 = (mapper & 0xF0) | (flags7_low & 0x0F)
    return magic + bytes([prg_banks, chr_banks, flags6, flags7]) + bytes(8)


def make_dummy_prg(size: int = FILE_EXPECTED_PRG_SIZE) -> bytes:
    return b"\x11" * size


def make_dummy_chr(size: int = FILE_EXPECTED_CHR_SIZE) -> bytes:
    return b"\x22" * size


def test_valid_header_loads_prg_and_chr():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    rom = ROM(make_header() + prg + chr_data)

    assert rom.header.magic == b"NES\x1a"
    assert rom.header.mapper == 4
    assert rom.prg == prg
    assert rom.chr == chr_data


def test_extract_rom_data(tmp_path):
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

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


def test_wrong_magic_is_rejected():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header(magic=b"\x1aSEN")
    with pytest.raises(ValueError, match="Invalid iNES header"):
        ROM(header + prg + chr_data)


def test_mirroring_bit_is_ignored():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header(flags6_low=0x01)
    rom = ROM(header + prg + chr_data)
    assert rom.header.mapper == 4


def test_trainer_is_skipped():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header(flags6_low=0x04)
    rom = ROM(header + b"\xff" * 512 + prg + chr_data)
    assert rom.prg == prg
    assert rom.chr == chr_data


def test_trailing_byte_is_rejected():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header()
    with pytest.raises(ValueError, match="Data size does not match header information"):
        ROM(header + prg + chr_data + b"\x00")


def test_wrong_mapper_is_rejected():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header(mapper=20)
    with pytest.raises(ValueError, match="This is not a valid Crystalis ROM"):
        ROM(header + prg + chr_data)


def test_wrong_prg_size_is_rejected():
    prg = make_dummy_prg(15 * HEADER_PRG_BANK_SIZE)
    chr_data = make_dummy_chr()

    header = make_header(prg_banks=15)
    with pytest.raises(ValueError, match="This is not a valid Crystalis ROM"):
        ROM(header + prg + chr_data)


def test_wrong_chr_size_is_rejected():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr(15 * HEADER_CHR_BANK_SIZE)

    header = make_header(chr_banks=15)
    with pytest.raises(ValueError, match="This is not a valid Crystalis ROM"):
        ROM(header + prg + chr_data)


def test_nes_2_marker_does_not_change_mapper():
    prg = make_dummy_prg()
    chr_data = make_dummy_chr()

    header = make_header(flags7_low=0x08)
    rom = ROM(header + prg + chr_data)
    assert rom.header.mapper == 4
