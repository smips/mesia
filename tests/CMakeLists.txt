# SPDX-License-Identifier: GPL-3.0-or-later

add_executable(mesia_tests
    version_test.cpp)
target_link_libraries(mesia_tests PRIVATE mesia::core Catch2::Catch2WithMain)
mesia_set_warnings(mesia_tests)
mesia_copy_sanitizer_runtime(mesia_tests)

include(Catch)
catch_discover_tests(mesia_tests DISCOVERY_MODE PRE_TEST)
