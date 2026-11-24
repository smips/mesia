// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once
#include <array>
#include "cartridge.hpp"

namespace mesia {
    class Mmc3 {
        public:
            explicit Mmc3(const Cartridge& cartridge) :
                cartridge(cartridge), bankControl(), irq(), horizontalMirroring(false), prgRamEnabled(false), prgRamWriteProtected(false) { };
            ~Mmc3() = default;
            void write(uint16_t address, uint8_t value);
            uint8_t read_prg(uint16_t cpu_address) const;
            uint8_t read_chr(uint16_t ppu_address) const;

        private:
            // Define a struct to represent the control registers at 0x8000 and 0x8001
            struct BankControl {
                uint8_t bankSelect;
                bool prgBankMode;
                bool chrA12Inversion;
                std::array<uint8_t, 8> registers;
            };

            struct Irq {
                uint8_t latch;
                uint8_t counter;
                bool reload;
                bool enabled;
            };

            const Cartridge& cartridge;
            BankControl bankControl; // Control registers for MMC3
            Irq irq; // IRQ control for MMC3
            bool horizontalMirroring; // Mirroring mode (horizontal or vertical)
            bool prgRamEnabled; // PRG RAM enable/disable flag
            bool prgRamWriteProtected; // PRG RAM write protection flag
            // Add methods and members for MMC3 functionality here
    };
} // namespace mesia
