// SPDX-License-Identifier: GPL-3.0-or-later

#include <cassert>
#include "mesia/mmc3.hpp"
#include "mesia/exceptions.hpp"

namespace mesia {
    void Mmc3::write(uint16_t address, uint8_t value) {
        // Implement the write logic for MMC3 here
        uint16_t registerAddress = address & 0xE001; // Mask to get the relevant register address
        switch(registerAddress) {
            case 0x8000:
                // Handle bank select register
                bankControl.bankSelect = value & 0x07; // Only the lower 3 bits are used
                bankControl.prgBankMode = (value & 0x40) != 0; // Bit 6 determines PRG bank mode
                bankControl.chrA12Inversion = (value & 0x80) != 0; // Bit 7 determines CHR A12 inversion
                break;
            case 0x8001:
                // Handle bank data register
                bankControl.registers[bankControl.bankSelect] = value;
                break;
            case 0xA000:
                // Handle mirroring control register
                horizontalMirroring = (value & 0x01) == 0; // Bit 0 determines mirroring mode
                break;
            case 0xA001:
                // Handle PRG RAM protect register
                prgRamEnabled = (value & 0x80) != 0; // Bit 7 enables/disables PRG RAM
                prgRamWriteProtected = (value & 0x40) != 0; // Bit 6 write protection
                break;
            case 0xC000:
                // Handle IRQ latch register
                irq.latch = value;
                break;
            case 0xC001:
                // Handle IRQ reload register
                irq.reload = true;
                break;
            case 0xE000:
                // Handle IRQ disable register
                irq.enabled = false;
                break;
            case 0xE001:
                // Handle IRQ enable register
                irq.enabled = true;
                break;
            default:
                assert(false && "Invalid MMC3 register address");
        }

    }

    uint8_t Mmc3::read_prg([[maybe_unused]] uint16_t cpu_address) const {
        // Implement the read logic for PRG ROM here

        // Need to decide how to handle the PRG mapping. Kind of need
        // an array of pointers to the selected PRG banks?
        throw NotImplementedException(__func__);
    }

    uint8_t Mmc3::read_chr([[maybe_unused]] uint16_t cpu_address) const {
        // Implement the read logic for CHR ROM here
        throw NotImplementedException(__func__);
    }
} // namespace mesia
