// SPDX-License-Identifier: GPL-3.0-or-later

#include <filesystem>
#include <fstream>
#include "mesia/cartridge.hpp"
#include "mesia/exceptions.hpp"

namespace mesia {
    Cartridge::Cartridge() {
        _prg.assign(0x40000, 0); // Reserve space for 256KB of PRG ROM
        _chr.assign(0x20000, 0); // Reserve space for 128KB of CHR ROM
    }

    bool Cartridge::load([[maybe_unused]] const std::string& path) {
        bool result = false;
        std::filesystem::path data_path(path);
        std::filesystem::path prg_path(data_path.parent_path() / PRG_FILENAME);
        std::filesystem::path chr_path(data_path.parent_path() / CHR_FILENAME);
        if(std::filesystem::exists(prg_path) &&
           std::filesystem::exists(chr_path) &&
           std::filesystem::file_size(prg_path) == _prg.size() &&
           std::filesystem::file_size(chr_path) == _chr.size()) {



            // Load the cartridge file into _prg and _chr
            // This is a placeholder for actual loading logic
            throw NotImplementedException();
        }

        return result;
    }

    bool Cartridge::read_prg(unsigned short address, uint8_t &value) const {
        value = address < _prg.size() ? _prg[address] : 0;
        return address < _prg.size();
    }

    bool Cartridge::read_chr(unsigned short address, uint8_t &value) const {
        value = address < _chr.size() ? _chr[address] : 0;
        return address < _chr.size();
    }


} // namespace mesia
