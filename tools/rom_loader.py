# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Final
from pick import pick
import os
from hashlib import sha1
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

ROM_PATH: Final[str] = "..\\roms"
FILE_EXPECTED_SIZE: Final[int] = 393232 # file size in bytes, including iNES header
FILE_EXPECTED_SHA1: Final[str] = "FD0DCDE4F1708B30D5C3DE1E463F1DDE89C5CB64" # SHA-1 hash of the ROM file
FILE_EXPECTED_CRC32: Final[str] = "1BD39032" # CRC32 hash of the ROM file


def check_directory(path) -> bool:
    return os.path.exists(path) and os.path.isdir(path)

def check_size(file_path) -> bool:
    return os.path.isfile(file_path) and os.path.getsize(file_path) == FILE_EXPECTED_SIZE

def check_file_sha1(file_path) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()
    hash_value = sha1(data).hexdigest()
    print(f"SHA-1 hash for {file_path}: {hash_value}")
    return hash_value == FILE_EXPECTED_SHA1

def check_file_crc32(file_path) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()
    crc32_value = crc32(data) & 0xffffffff
    print(f"CRC32 hash for {file_path}: {crc32_value:08x}")
    return f"{crc32_value:08x}" == FILE_EXPECTED_CRC32

def check_file_header(file_path):
    # Placeholder for ROM header reading
    raise NotImplementedError("ROM header reading is not implemented yet.")


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
        print("Calculating SHA-1 hash...")
        if not check_file_sha1(file_path):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The selected ROM does not have the expected SHA-1 hash.{bcolors.ENDC}")
            return

        # Check file CRC32
        print("Calculating CRC32 hash...")
        if not check_file_crc32(file_path):
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: The selected ROM does not have the expected CRC32 hash.{bcolors.ENDC}")
            return

        # Reading the ROM Header
        print("Reading ROM header...")
        try:
            check_file_header(file_path)
        except NotImplementedError:
            print(f"{bcolors.BOLD}{bcolors.FAIL}ERROR: ROM header reading is not implemented yet.{bcolors.ENDC}")
            return

    else:
        print("No files found in the directory.")

if __name__ == "__main__":
    main()