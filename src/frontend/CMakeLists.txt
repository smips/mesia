# SPDX-License-Identifier: GPL-3.0-or-later

add_executable(mesia main.cpp)
target_link_libraries(mesia PRIVATE mesia::core SDL3::SDL3)
mesia_set_warnings(mesia)
mesia_copy_sanitizer_runtime(mesia)

if(MESIA_BUILD_TESTS)
    # Opens the window on SDL's headless driver, so it runs on CI machines.
    add_test(NAME frontend_smoke_test COMMAND mesia --smoke-test)
    set_tests_properties(frontend_smoke_test PROPERTIES ENVIRONMENT SDL_VIDEO_DRIVER=dummy)
endif()
