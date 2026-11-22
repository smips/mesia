// SPDX-License-Identifier: GPL-3.0-or-later

#include <catch2/catch_test_macros.hpp>

#include "mesia/version.hpp"

TEST_CASE("version string comes from the CMake project", "[version]") {
    REQUIRE_FALSE(mesia::version().empty());
    REQUIRE(mesia::version().starts_with("0."));
}
