// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include <string_view>

namespace mesia {

// Engine version, taken from the top-level CMake project() call.
std::string_view version() noexcept;

} // namespace mesia
