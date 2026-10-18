# SPDX-License-Identifier: GPL-3.0-or-later

# Strict warnings, treated as errors. Applied per target so third-party
# code fetched by Dependencies.cmake is not affected.
function(mesia_set_warnings target)
    if(MSVC)
        target_compile_options(${target} PRIVATE
            /W4 /WX /permissive- /utf-8
            /w14242 /w14254 /w14263 /w14265 /w14287 /w14296 /w14311
            /w14545 /w14546 /w14547 /w14549 /w14555 /w14619 /w14640
            /w14826 /w14905 /w14906 /w14928)
    else()
        target_compile_options(${target} PRIVATE
            -Wall -Wextra -Wpedantic -Werror
            -Wshadow -Wconversion -Wsign-conversion -Wold-style-cast
            -Wcast-align -Wunused -Woverloaded-virtual -Wnull-dereference
            -Wdouble-promotion -Wformat=2 -Wimplicit-fallthrough)
    endif()
endfunction()
