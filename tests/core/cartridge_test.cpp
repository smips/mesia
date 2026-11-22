// SPDX-License-Identifier: GPL-3.0-or-later

#include <catch2/catch_test_macros.hpp>
#include <string>
#include "mesia/cartridge.hpp"

namespace mesia::test {
    TEST_CASE("Cartridge class can be instantiated", "[cartridge]") {
        mesia::Cartridge cartridge;
        REQUIRE(true); // If we reach this point, the test passes
    }
};
