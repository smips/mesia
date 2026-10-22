# SPDX-License-Identifier: GPL-3.0-or-later

##########################################################################################
# rom_loader.py
# This script is used to load and validate a Crystalis NES ROM file.
# It checks the ROM's header, size, and hash values to ensure that it is a valid Crystalis ROM.
# Once the ROM is validated, the script extracts the PRG and CHR data from the ROM file.
#
##########################################################################################


import hashlib
import os
import sys
from binascii import crc32
from typing import Final

from pick import pick

ROM_PATH: Final[str] = "..\\roms"
# ROM_PATH: Final[str] = "roms"

# Expected Sizes
FILE_EXPECTED_HEADER_SIZE: Final[int] = 16  # header size in bytes
FILE_EXPECTED_PRG_SIZE: Final[int] = 262144  # PRG ROM size in bytes
FILE_EXPECTED_CHR_SIZE: Final[int] = 131072  # CHR ROM size in bytes

# Expected Hashes
ROM_EXPECTED_SHA1: Final[str] = (
    "8A49FE60B6A151C055A63639894CD366935A7EE9"  # SHA-1 hash of the ROM data (PRG + CHR)
)
ROM_EXPECTED_CRC32: Final[str] = "1335CB05"  # CRC32 hash of the ROM data (PRG + CHR)

# Expected Header Values
HEADER_EXPECTED_MAPPER: Final[int] = 4  # Expected mapper number for the ROM file
HEADER_PRG_BANK_SIZE: Final[int] = 16384  # PRG bank size in bytes (16KB)
HEADER_CHR_BANK_SIZE: Final[int] = 8192  # CHR bank size in bytes (8KB)


class Colors:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class INesHeader:
    def __init__(self, data: bytes):
        if len(data) != FILE_EXPECTED_HEADER_SIZE:
            raise ValueError("iNES header must be 16 bytes long.")
        self.data = data
        self.magic = data[0:4]
        self.prg_rom_size = data[4]
        self.chr_rom_size = data[5]
        self.mapper = (data[6] >> 4) | (data[7] & 0xF0)
        self.trainer = bool(data[6] & 0x04)

    def is_valid(self) -> bool:
        return self.magic == b"NES\x1a"

    def is_crystalis(self) -> bool:
        return (
            self.is_valid()
            and self.prg_rom_size * HEADER_PRG_BANK_SIZE == FILE_EXPECTED_PRG_SIZE
            and self.chr_rom_size * HEADER_CHR_BANK_SIZE == FILE_EXPECTED_CHR_SIZE
            and self.mapper == HEADER_EXPECTED_MAPPER
        )


class ROM:
    header: INesHeader
    prg: bytes
    chr: bytes

    def __init__(self, data: bytes):
        if len(data) <= FILE_EXPECTED_HEADER_SIZE:
            raise ValueError("Data is too small.")
        self.header = INesHeader(data[:FILE_EXPECTED_HEADER_SIZE])
        if not self.header.is_valid():
            raise ValueError("Invalid iNES header.")
        if not self.header.is_crystalis():
            raise ValueError("This is not a valid Crystalis ROM.")
        trainer_size = 512 if self.header.trainer else 0
        prg_start = FILE_EXPECTED_HEADER_SIZE + trainer_size
        prg_end = prg_start + self.header.prg_rom_size * HEADER_PRG_BANK_SIZE
        chr_end = prg_end + self.header.chr_rom_size * HEADER_CHR_BANK_SIZE
        if len(data) != chr_end:
            raise ValueError("Data size does not match header information.")
        self.prg = data[prg_start:prg_end]  # Populate PRG ROM data
        self.chr = data[prg_end:chr_end]  # Populate CHR ROM data

    def print_info(self):
        print(f"Header Magic:\t{self.header.magic}")
        print(f"PRG ROM Size:\t{len(self.prg)} bytes")
        print(f"CHR ROM Size:\t{len(self.chr)} bytes")
        print(f"Mapper:\t{self.header.mapper}")


def print_fail(message: str):
    print(f"{Colors.BOLD}{Colors.FAIL}ERROR: {message}{Colors.ENDC}")


def print_success(message: str):
    print(f"{Colors.BOLD}{Colors.OKGREEN}SUCCESS: {message}{Colors.ENDC}")


def check_rom_sha1(rom: ROM) -> tuple[bool, str]:
    digest = hashlib.sha1()
    digest.update(rom.prg)
    digest.update(rom.chr)
    digest_str = digest.hexdigest().upper()
    return digest_str == ROM_EXPECTED_SHA1, digest_str


def check_rom_crc32(rom: ROM) -> tuple[bool, str]:
    crc32_value = crc32(rom.prg)
    crc32_value = crc32(rom.chr, crc32_value)
    crc32_str = f"{crc32_value:08X}"
    return crc32_str == ROM_EXPECTED_CRC32, crc32_str


def main():
    if not os.path.isdir(ROM_PATH):
        print_fail(f"Directory {ROM_PATH} does not exist.")
        sys.exit(1)

    roms = os.listdir(ROM_PATH)
    if len(roms) > 0:
        option, index = pick(roms, "Select a ROM to extract:")
        file_path = os.path.join(ROM_PATH, option)
        print(f"You selected: {index}: {option}")
        print("\n\nReading ROM...")

        # Read the selected ROM file
        with open(file_path, "rb") as f:
            data = f.read()

        try:
            rom = ROM(data)
        except ValueError as e:
            print_fail(str(e))
            sys.exit(1)

        # Check ROM SHA-1
        print("Calculating ROM data SHA-1 hash...")
        res, sha1_hash = check_rom_sha1(rom)
        if not res:
            print_fail("The ROM data does not have the expected SHA-1 hash.")
            print(f"\tExpected:\t{ROM_EXPECTED_SHA1}")
            print(f"\tCalculated:\t{sha1_hash}")
            sys.exit(1)

        # Check ROM CRC32
        print("Calculating ROM data CRC32 hash...")
        res, crc32_hash = check_rom_crc32(rom)
        if not res:
            print_fail("The ROM data does not have the expected CRC32 hash.")
            print(f"\tExpected:\t{ROM_EXPECTED_CRC32}")
            print(f"\tCalculated:\t{crc32_hash}")
            sys.exit(1)

        print_success("ROM data is valid!")
        rom.print_info()

        print("Extracting PRG and CHR data from ROM...")

    else:
        print_fail("No files found in the directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
