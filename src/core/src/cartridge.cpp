// SPDX-License-Identifier: GPL-3.0-or-later

#include "mesia/cartridge.hpp"
#include "mesia/not_implemented.hpp"

namespace mesia {
    Cartridge::Cartridge() {
        _prg.assign(0x40000, 0); // Reserve space for 256KB of PRG ROM
        _chr.assign(0x20000, 0); // Reserve space for 128KB of CHR ROM
    }

    bool Cartridge::load([[maybe_unused]] const std::string& filename) {
        // Implementation for loading cartridge file
        throw NotImplementedException();
    }

    bool Cartridge::read_prg(unsigned short address, unsigned char &value) const {
        value = address < sizeof(_prg) ? _prg[address] : 0;
        return address < sizeof(_prg);
    }

    bool Cartridge::read_chr(unsigned short address, unsigned char &value) const {
        value = address < sizeof(_chr) ? _chr[address] : 0;
        return address < sizeof(_chr);
    }


} // namespace mesia
