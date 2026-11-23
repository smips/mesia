// SPDX-License-Identifier: GPL-3.0-or-later

#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_string.hpp>
#include <catch2/matchers/catch_matchers_exception.hpp>
#include <filesystem>
#include <fstream>
#include <string>
#include "temp_dir.hpp"
#include "mesia/cartridge.hpp"

using Catch::Matchers::ContainsSubstring;
using Catch::Matchers::MessageMatches;


namespace mesia::test {
    static void create_test_data(const std::string& path, bool prg = true, bool chr = true,
        size_t prg_size = 0x40000, size_t chr_size = 0x20000) {
        std::filesystem::path dir_path(path);

        if(prg) {
            std::ofstream prg_file(dir_path / "prg.bin", std::ios::binary);
            REQUIRE(prg_file);
            for(size_t i = 0; i < prg_size; ++i) {
                prg_file.put(static_cast<char>(i ^ (i >> 8))); // Fill PRG with a pattern
            }
            prg_file.close();
        }

        if(chr) {
            std::ofstream chr_file(dir_path / "chr.bin", std::ios::binary);
            REQUIRE(chr_file);
            for(size_t i = 0; i < chr_size; ++i) {
                chr_file.put(static_cast<char>(i ^ (i >> 8))); // Fill CHR with a pattern
            }
            chr_file.close();
        }
    }

    TEST_CASE("Cartridge class can be instantiated", "[cartridge]") {
        mesia::Cartridge cartridge;
        REQUIRE(true); // If we reach this point, the test passes
    }

    TEST_CASE("Cartridge class can load PRG and CHR data", "[cartridge]") {
        mesia::Cartridge cartridge;
        mesia::test::TempDir temp_dir;

        create_test_data(temp_dir.path().string());

        REQUIRE_NOTHROW(cartridge.load(temp_dir.path().string()));

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

    TEST_CASE("Cartridge class throws error on missing PRG or CHR files", "[cartridge]") {
        mesia::Cartridge cartridge;
        mesia::test::TempDir temp_dir;

        SECTION("Testing PRG file missing") {
            // Create only CHR file
            create_test_data(temp_dir.path().string(), false, true);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("PRG ROM file not found")));
        }

        SECTION("Testing CHR file missing") {
            // Create only PRG file
            create_test_data(temp_dir.path().string(), true, false);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("CHR ROM file not found")));
        }
    }

    TEST_CASE("Cartridge class throws error on incorrect file sizes", "[cartridge]") {
        mesia::Cartridge cartridge;
        mesia::test::TempDir temp_dir;

        SECTION("Testing PRG file with incorrect size (-1)") {
            // Create PRG file with incorrect size
            create_test_data(temp_dir.path().string(), true, true, 0x3FFFF, 0x20000);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("PRG ROM file size does not match expected size")));
        }

        SECTION("Testing PRG file with incorrect size (+1)") {
            // Create PRG file with incorrect size
            create_test_data(temp_dir.path().string(), true, true, 0x40001, 0x20000);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("PRG ROM file size does not match expected size")));
        }

        SECTION("Testing CHR file with incorrect size (-1)") {
            // Create CHR file with incorrect size
            create_test_data(temp_dir.path().string(), true, true, 0x40000, 0x1FFFF);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("CHR ROM file size does not match expected size")));
        }

        SECTION("Testing CHR file with incorrect size (+1)") {
            // Create CHR file with incorrect size
            create_test_data(temp_dir.path().string(), true, true, 0x40000, 0x20001);
            REQUIRE_THROWS_MATCHES(cartridge.load(temp_dir.path().string()), mesia::CartridgeError, MessageMatches(ContainsSubstring("CHR ROM file size does not match expected size")));
        }
    }

}
