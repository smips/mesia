// SPDX-License-Identifier: GPL-3.0-or-later

#include <filesystem>
#include <fstream>
#include "mesia/cartridge.hpp"

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

        std::error_code ec;
        // Check if the files exist and have the expected sizes
        bool exists = std::filesystem::exists(prg_path, ec);
        if(ec) {
            throw CartridgeError("Error checking PRG ROM file existence. Path: " + prg_path.string() + ", Error: " + ec.message());
        }
        if(!exists) {
            throw CartridgeError("PRG ROM file not found. Path: " + prg_path.string());
        }

        exists = std::filesystem::exists(chr_path, ec);
        if(ec) {
            throw CartridgeError("Error checking CHR ROM file existence. Path: " + chr_path.string() + ", Error: " + ec.message());
        }
        if(!exists) {
            throw CartridgeError("CHR ROM file not found. Path: " + chr_path.string());
        }

        auto prg_size = std::filesystem::file_size(prg_path, ec);
        if(ec) {
            throw CartridgeError("Error checking PRG ROM file size. Path: " + prg_path.string() + ", Error: " + ec.message());
        }
        if(prg_size != _prg.size()) {
            throw CartridgeError("PRG ROM file size does not match expected size. Path: " + prg_path.string() + ", Expected Size: " + std::to_string(_prg.size()) + ", Actual Size: " + std::to_string(prg_size));
        }

        auto chr_size = std::filesystem::file_size(chr_path, ec);
        if(ec) {
            throw CartridgeError("Error checking CHR ROM file size. Path: " + chr_path.string() + ", Error: " + ec.message());
        }
        if(chr_size != _chr.size()) {
            throw CartridgeError("CHR ROM file size does not match expected size. Path: " + chr_path.string() + ", Expected Size: " + std::to_string(_chr.size()) + ", Actual Size: " + std::to_string(chr_size));
        }

        // Open the files and read the data into the vectors
        std::ifstream prg_file(prg_path, std::ios::binary);
        std::ifstream chr_file(chr_path, std::ios::binary);
        if(!prg_file.read(reinterpret_cast<char*>(_prg.data()), static_cast<std::streamsize>(_prg.size()))) {
            throw CartridgeError("Failed to read PRG ROM data. Path: " + prg_path.string());
        }
        if(!chr_file.read(reinterpret_cast<char*>(_chr.data()), static_cast<std::streamsize>(_chr.size()))) {
            throw CartridgeError("Failed to read CHR ROM data. Path: " + chr_path.string());
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
