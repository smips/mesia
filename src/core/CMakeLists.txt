# SPDX-License-Identifier: GPL-3.0-or-later

add_library(mesia_core STATIC
    src/version.cpp)
add_library(mesia::core ALIAS mesia_core)

target_include_directories(mesia_core PUBLIC include)
target_compile_features(mesia_core PUBLIC cxx_std_20)
mesia_set_warnings(mesia_core)

configure_file(version_config.hpp.in ${CMAKE_CURRENT_BINARY_DIR}/generated/mesia/version_config.hpp @ONLY)
target_include_directories(mesia_core PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/generated)
