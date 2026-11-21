// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once
#include <string>
#include <vector>

namespace mesia {
    class Cartridge {
        private:
            std::vector<unsigned char> _prg; // PRG ROM data
            std::vector<unsigned char> _chr; // CHR ROM data

        public:
            Cartridge();
            ~Cartridge() = default;
            bool load(const std::string& filename);
            bool read_prg(unsigned short address, unsigned char &value) const;
            bool read_chr(unsigned short address, unsigned char &value) const;
    };
} // namespace mesia
