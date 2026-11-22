// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once
#include <string>
#include <vector>
#include <cstdint>
#include <stdexcept>

namespace mesia {
    class CartridgeError : public std::runtime_error {
        public:
            CartridgeError(const std::string& message) : std::runtime_error(message) { };
    }; // class CartridgeError

    class Cartridge {
        private:
            std::vector<uint8_t> _prg; // PRG ROM data
            std::vector<uint8_t> _chr; // CHR ROM data
            static constexpr const char* PRG_FILENAME = "prg.bin";
            static constexpr const char* CHR_FILENAME = "chr.bin";

        public:
            Cartridge();
            ~Cartridge() = default;
            void load(const std::string& path);
            bool read_prg(uint32_t address, uint8_t &value) const;
            bool read_chr(uint32_t address, uint8_t &value) const;
    };
} // namespace mesia
