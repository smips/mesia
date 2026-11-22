// SPDX-License-Identifier: GPL-3.0-or-later

#include <catch2/catch_test_macros.hpp>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include "temp_dir.hpp"
#include "mesia/cartridge.hpp"


namespace mesia::test {
    static void create_test_data(const std::string& path) {
        std::filesystem::create_directory(path);
        std::ofstream prg_file(path + "\\prg.bin", std::ios::binary);
        std::ofstream chr_file(path + "\\chr.bin", std::ios::binary);
        for(size_t i = 0; i < 0x40000; ++i) {
            prg_file.put(static_cast<char>(i ^ (i >> 8))); // Fill PRG with a pattern
            if(i < 0x20000) {
                chr_file.put(static_cast<char>(i ^ (i >> 8))); // Fill CHR with a pattern
            }
        }
        prg_file.close();
        chr_file.close();
    }

    TEST_CASE("Cartridge class can be instantiated", "[cartridge]") {
        mesia::Cartridge cartridge;
        REQUIRE(true); // If we reach this point, the test passes
    }

    TEST_CASE("Cartridge class can load PRG and CHR data", "[cartridge]") {
        mesia::Cartridge cartridge;
        mesia::test::TempDir temp_dir;
        std::string test_data_path = temp_dir.path().string() + "\\test_data";
        std::cout << "Test data path: " << test_data_path << std::endl;

        create_test_data(test_data_path);

        REQUIRE_NOTHROW(cartridge.load(test_data_path));

        uint8_t value;
        REQUIRE_FALSE(cartridge.read_prg(0x40000, value)); // Out of bounds
        REQUIRE_FALSE(cartridge.read_chr(0x20000, value)); // Out of bounds
        REQUIRE(cartridge.read_prg(0x0000, value));
        REQUIRE(value == 0x00);
        REQUIRE(cartridge.read_prg(0x3FFFF, value));
        REQUIRE(value == ((0x3FFFF ^ (0x3FFFF >> 8)) & 0xFF));
        REQUIRE(cartridge.read_chr(0x0000, value));
        REQUIRE(value == 0x00);
        REQUIRE(cartridge.read_chr(0x1FFFF, value));
        REQUIRE(value == ((0x1FFFF ^ (0x1FFFF >> 8)) & 0xFF));
    }
};
