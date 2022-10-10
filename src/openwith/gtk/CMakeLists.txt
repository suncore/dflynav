cmake_minimum_required(VERSION 3.0)
project(gtk-open-with C CXX)

# Use the package PkgConfig to detect GTK+ headers/library files
find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK REQUIRED gtkmm-3.0)

add_executable(gtk-open-with gtk-open-with.cpp)

target_link_directories(gtk-open-with PRIVATE ${GTK_LIBRARY_DIRS})
target_include_directories(gtk-open-with PRIVATE ${GTK_INCLUDE_DIRS})
target_link_libraries(gtk-open-with PRIVATE ${GTK_LIBRARIES})