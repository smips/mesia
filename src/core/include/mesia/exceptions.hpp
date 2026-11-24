// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <string>
#include <stdexcept>

namespace mesia {

    class NotImplementedException : public std::logic_error {
        public:
            NotImplementedException(const char * const func) : std::logic_error(func + std::string(" not yet implemented")) { };
    }; // class NotImplementedException

} // namespace mesia
