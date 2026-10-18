// SPDX-License-Identifier: GPL-3.0-or-later

#include "mesia/version.hpp"

#include "mesia/version_config.hpp"

namespace mesia {

std::string_view version() noexcept {
    return MESIA_VERSION_STRING;
}

} // namespace mesia
