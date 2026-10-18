// SPDX-License-Identifier: GPL-3.0-or-later

#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

#include <cstdlib>
#include <string>
#include <string_view>

#include "mesia/version.hpp"

namespace {

constexpr int kNesWidth = 256;
constexpr int kNesHeight = 240;
constexpr int kInitialScale = 3;

// With --smoke-test the window closes itself after this many frames, so the
// build can be checked without someone clicking it shut.
constexpr int kSmokeTestFrames = 60;

} // namespace

int main(int argc, char* argv[]) {
    bool smoke_test = false;
    for (int i = 1; i < argc; ++i) {
        if (std::string_view{argv[i]} == "--smoke-test") {
            smoke_test = true;
        }
    }

    if (!SDL_Init(SDL_INIT_VIDEO)) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "SDL_Init failed: %s", SDL_GetError());
        return EXIT_FAILURE;
    }

    const std::string title = "Mesia " + std::string{mesia::version()};
    SDL_Window* window = nullptr;
    SDL_Renderer* renderer = nullptr;
    if (!SDL_CreateWindowAndRenderer(title.c_str(), kNesWidth * kInitialScale,
                                     kNesHeight * kInitialScale, SDL_WINDOW_RESIZABLE,
                                     &window, &renderer)) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Window creation failed: %s", SDL_GetError());
        SDL_Quit();
        return EXIT_FAILURE;
    }

    // Draw in NES coordinates; SDL scales to the window, keeping the aspect.
    SDL_SetRenderLogicalPresentation(renderer, kNesWidth, kNesHeight,
                                     SDL_LOGICAL_PRESENTATION_LETTERBOX);
    SDL_SetRenderVSync(renderer, 1);

    bool running = true;
    int frames = 0;
    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT) {
                running = false;
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
        SDL_RenderClear(renderer);
        SDL_RenderPresent(renderer);

        ++frames;
        if (smoke_test && frames >= kSmokeTestFrames) {
            running = false;
        }
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return EXIT_SUCCESS;
}
