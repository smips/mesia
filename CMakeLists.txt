# SPDX-License-Identifier: GPL-3.0-or-later

cmake_minimum_required(VERSION 3.25)

project(Mesia
    VERSION 0.1.0
    DESCRIPTION "An engine for playing Crystalis with your own ROM"
    LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Put every executable and DLL in one directory so SDL3.dll and the
# sanitizer runtime are found without touching PATH.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

option(MESIA_SANITIZERS "Enable sanitizers in Debug builds" ON)
option(MESIA_BUILD_TESTS "Build the Catch2 test suite" ON)
option(MESIA_BUILD_FRONTEND "Build the SDL3 frontend" ON)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(Warnings)
include(Sanitizers)   # global, so third-party code is instrumented consistently
include(Dependencies)

add_subdirectory(src/core)
if(MESIA_BUILD_FRONTEND)
    add_subdirectory(src/frontend)
endif()

if(MESIA_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
