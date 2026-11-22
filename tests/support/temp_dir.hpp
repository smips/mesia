// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once
#include <filesystem>
#include <random>
#include <string>

namespace mesia::test {
    class TempDir {
        public:
            TempDir() {
                std::random_device rd;
                _path = std::filesystem::temp_directory_path();
                _path.append("/mesia_test_");
                _path.append(std::to_string(rd()));
                std::filesystem::create_directory(_path);
            }

            ~TempDir() {
                std::error_code ec;
                std::filesystem::remove_all(_path, ec);
            }

            TempDir(const TempDir&) = delete;

            TempDir& operator=(const TempDir&) = delete;

            const std::filesystem::path& path() const {
                return _path;
            }
        private:
            std::filesystem::path _path;
    };
} // namespace mesia::test
