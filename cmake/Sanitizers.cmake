# SPDX-License-Identifier: GPL-3.0-or-later

# Sanitizers for Debug builds.
#   GCC/Clang: AddressSanitizer + UndefinedBehaviorSanitizer
#   MSVC:      AddressSanitizer (the only one MSVC provides)
# Applied globally so every library linked into a target is built the same
# way; MSVC refuses to link ASan and non-ASan C++ objects together.
if(NOT MESIA_SANITIZERS)
    return()
endif()

if(MSVC)
    add_compile_options("$<$<CONFIG:Debug>:/fsanitize=address>")
    add_link_options("$<$<CONFIG:Debug>:/INCREMENTAL:NO>")
    # /RTC1 is incompatible with ASan; drop it from the default Debug flags.
    foreach(lang C CXX)
        string(REPLACE "/RTC1" "" CMAKE_${lang}_FLAGS_DEBUG "${CMAKE_${lang}_FLAGS_DEBUG}")
    endforeach()

    # The ASan runtime DLL lives next to the compiler; copy it beside our
    # executables so they run outside a Developer Command Prompt.
    get_filename_component(_cl_dir "${CMAKE_CXX_COMPILER}" DIRECTORY)
    file(GLOB MESIA_ASAN_RUNTIME "${_cl_dir}/clang_rt.asan_dynamic-*.dll")
else()
    set(_flags -fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=undefined)
    add_compile_options("$<$<CONFIG:Debug>:${_flags}>")
    add_link_options("$<$<CONFIG:Debug>:-fsanitize=address,undefined>")
endif()

# Copies the sanitizer runtime next to an executable when one is needed.
function(mesia_copy_sanitizer_runtime target)
    if(MSVC AND MESIA_ASAN_RUNTIME)
        add_custom_command(TARGET ${target} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E $<IF:$<CONFIG:Debug>,copy_if_different,true>
                    "${MESIA_ASAN_RUNTIME}" "$<TARGET_FILE_DIR:${target}>")
    endif()
endfunction()
