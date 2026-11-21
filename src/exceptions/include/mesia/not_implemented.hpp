// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <stdexcept>

namespace mesia {

    class NotImplementedException : public std::logic_error {
        public:
            NotImplementedException() : std::logic_error("Function not yet implemented") { };
    }; // class NotImplementedException

} // namespace mesia
