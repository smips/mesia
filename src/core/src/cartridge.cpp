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

    void Cartridge::load(const std::string& path) {
        // Construct the paths to the PRG and CHR files based on the provided path
        const std::filesystem::path data_path(path);
        const std::filesystem::path prg_path(data_path / PRG_FILENAME);
        const std::filesystem::path chr_path(data_path / CHR_FILENAME);

        // Check if the files exist and have the expected sizes
        if(!std::filesystem::exists(prg_path)) {
            throw CartridgeError("PRG ROM file not found");
        }
        if(!std::filesystem::exists(chr_path)) {
            throw CartridgeError("CHR ROM file not found");
        }
        if(std::filesystem::file_size(prg_path) != _prg.size()) {
            throw CartridgeError("PRG ROM file size does not match expected size");
        }
        if(std::filesystem::file_size(chr_path) != _chr.size()) {
            throw CartridgeError("CHR ROM file size does not match expected size");
        }

        // Open the files and read the data into the vectors
        std::ifstream prg_file(prg_path, std::ios::binary);
        std::ifstream chr_file(chr_path, std::ios::binary);
        if(!prg_file.read(reinterpret_cast<char*>(_prg.data()), _prg.size())) {
            throw CartridgeError("Failed to read PRG ROM data");
        }
        if(!chr_file.read(reinterpret_cast<char*>(_chr.data()), _chr.size())) {
            throw CartridgeError("Failed to read CHR ROM data");
        }
    }

    bool Cartridge::read_prg(uint32_t address, uint8_t &value) const {
        value = address < _prg.size() ? _prg[address] : 0;
        return address < _prg.size();
    }

    bool Cartridge::read_chr(uint32_t address, uint8_t &value) const {
        value = address < _chr.size() ? _chr[address] : 0;
        return address < _chr.size();
    }


} // namespace mesia
