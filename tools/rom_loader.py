# SPDX-License-Identifier: GPL-3.0-or-later

import hashlib
from typing import Final
from pick import pick
import os
from binascii import crc32

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class iNesHeader:
    def __init__(self, data: bytes):
        if len(data) != 16:
            raise ValueError("iNES header must be 16 bytes long.")
        self.data = data
        self.magic = data[0:4]
        self.prg_rom_size = data[4]
        self.chr_rom_size = data[5]
        self.flags6 = data[6]
        self.flags7 = data[7]
        self.prg_ram_size = data[8]
        self.flags9 = data[9]
        self.flags10 = data[10]
        self.reserved = data[11:16]

    def is_valid(self) -> bool:
        return self.magic == b'NES\x1a'

class ROM_params:
    def __init__(self, prg_size: int, chr_size: int):
        self.prg_size = prg_size    # PRG ROM size in bytes
        self.chr_size = chr_size    # CHR ROM size in bytes

class ROM:
    header: iNesHeader
    prg: bytes
    chr: bytes
    
    def __init__(self, data: bytes = None, params: ROM_params = None):
        if data is not None and params is not None:
            if len(data) != (16 + params.prg_size + params.chr_size):
                raise ValueError("Data size does not match expected size.")
            self.header = iNesHeader(data[:16])
            self.prg = data[16:(16 + params.prg_size)]  # PRG ROM size in bytes
            self.chr = data[(16 + params.prg_size):(16 + params.prg_size + params.chr_size)]  # CHR ROM size in bytes
        else:
            raise ValueError("Either data or params must be provided to initialize the ROM.")
        
    def print_info(self):
        print(f"Header: {self.header.data}")
        print(f"PRG ROM Size: {len(self.prg)} bytes")
        print(f"CHR ROM Size: {len(self.chr)} bytes")
     
ROM_PATH: Final[str] = "..\\roms"
# ROM_PATH: Final[str] = "roms"

# Expected Sizes
FILE_EXPECTED_HEADER_SIZE: Final[int] = 16 # header size in bytes
FILE_EXPECTED_PRG_SIZE: Final[int] = 262144 # PRG ROM size in bytes
FILE_EXPECTED_CHR_SIZE: Final[int] = 131072 # CHR ROM size in bytes
FILE_EXPECTED_SIZE: Final[int] = FILE_EXPECTED_HEADER_SIZE + FILE_EXPECTED_PRG_SIZE + FILE_EXPECTED_CHR_SIZE # file size in bytes, including iNES header

# Expected Hashes
FILE_EXPECTED_SHA1: Final[str] = "C9144B473AC2A3B9BF3EA8054AFF565460E5B2D4" # SHA-1 hash of the ROM file
FILE_EXPECTED_CRC32: Final[str] = "F8F1865D" # CRC32 hash of the ROM file
ROM_EXPECTED_SHA1: Final[str] = "8A49FE60B6A151C055A63639894CD366935A7EE9" # SHA-1 hash of the ROM data (PRG + CHR)
ROM_EXPECTED_CRC32: Final[str] = "1335CB05" # CRC32 hash of the ROM data (PRG + CHR)

# Expected Header Values
HEADER_EXPECTED_VALUE: Final[bytes] = b"\x4E\x45\x53\x1A\x10\x10\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00" # Expected iNES header values for the ROM file

def check_directory(path) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

def check_size(file_path) -> bool:
    return os.path.isfile(file_path) and os.path.getsize(file_path) == FILE_EXPECTED_SIZE

def get_rom(file_path) -> ROM:
    par: ROM_params = ROM_params(FILE_EXPECTED_PRG_SIZE, FILE_EXPECTED_CHR_SIZE)
    with open(file_path, "rb") as f:
        data = f.read()
    return ROM(data=data, params=par)

def check_file_sha1(file_path) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()
    digest = hashlib.sha1()
    digest.update(data)
    print(f"SHA-1 hash for {file_path}: {digest.hexdigest().upper()}")
    return digest.hexdigest().upper() == FILE_EXPECTED_SHA1

def check_file_crc32(file_path) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()
    crc32_value = crc32(data) & 0xffffffff
    print(f"CRC32 hash for {file_path}: {crc32_value:08X}")
    return f"{crc32_value:08x}".upper() == FILE_EXPECTED_CRC32

def check_rom_sha1(rom: ROM) -> bool:
    digest = hashlib.sha1()
    digest.update(rom.prg)
    digest.update(rom.chr)
    print(f"SHA-1 hash for ROM data: {digest.hexdigest().upper()}")
    return digest.hexdigest().upper() == ROM_EXPECTED_SHA1

def check_rom_crc32(rom: ROM) -> bool:
    crc32_value = crc32(rom.prg) & 0xffffffff
    crc32_value = crc32(rom.chr, crc32_value) & 0xffffffff
    print(f"CRC32 hash for ROM data: {crc32_value:08X}")
    return f"{crc32_value:08x}".upper() == ROM_EXPECTED_CRC32

def check_rom_header(rom: ROM) -> bool:
    if rom is not None and rom.header is not None:
        return rom.header.is_valid()
    else:
        return False
    
def check_rom_header_values(rom: ROM) -> bool:
    if rom is not None and rom.header is not None:
        return rom.header == HEADER_EXPECTED_VALUE
    else:
        return False

def main():
    if not check_directory(ROM_PATH):
        print(f"Error: Directory {ROM_PATH} does not exist.")
        return

    roms = os.listdir(ROM_PATH)
    if len(roms) > 0:
        option, index = pick(roms, "Select a ROM to extract:")
        file_path = os.path.join(ROM_PATH, option)
        print(f"You selected: {index}: {option}")
        print("\n\nReading ROM...")
        
        # Check the size of the selected ROM file
        if not check_size(file_path):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The selected ROM does not have the expected size.{bcolors.ENDC}")
            return
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}The selected ROM has the expected size of {FILE_EXPECTED_SIZE} bytes.{bcolors.ENDC}")
        
        # Check file SHA-1
        print("Calculating SHA-1 hash of file...")
        if not check_file_sha1(file_path):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The selected ROM does not have the expected SHA-1 hash.{bcolors.ENDC}")
            return

        # Check file CRC32
        print("Calculating CRC32 hash of file...")
        if not check_file_crc32(file_path):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The selected ROM does not have the expected CRC32 hash.{bcolors.ENDC}")
            return

        rom = get_rom(file_path)
        
        # Check ROM SHA-1
        print("Calculating ROM data SHA-1 hash...")
        if not check_rom_sha1(rom):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The ROM data does not have the expected SHA-1 hash.{bcolors.ENDC}")
            return
        
        # Check ROM CRC32
        print("Calculating ROM data CRC32 hash...")
        if not check_rom_crc32(rom):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The ROM data does not have the expected CRC32 hash.{bcolors.ENDC}")
            return

        # Check ROM header is valid
        print("Checking if ROM header is valid...")
        if not check_rom_header(rom):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The ROM header is invalid.{bcolors.ENDC}")
            return
        else:
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}The ROM header is valid.{bcolors.ENDC}")
            rom.print_info()
        
        # Validate ROM header is correct
        if not check_rom_header_values(rom):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The ROM header values are not as expected.{bcolors.ENDC}")
            return
        else:
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}The ROM header values are as expected.{bcolors.ENDC}")

    else:
        print("No files found in the directory.")

if __name__ == "__main__":
    main()