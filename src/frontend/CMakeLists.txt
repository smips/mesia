# SPDX-License-Identifier: GPL-3.0-or-later

add_executable(mesia main.cpp)
target_link_libraries(mesia PRIVATE mesia::core SDL3::SDL3)
mesia_set_warnings(mesia)
mesia_copy_sanitizer_runtime(mesia)
