cmake_minimum_required(VERSION 3.0.0)
project(tyr C CXX)

set(BACKEND "llvm" CACHE STRING "Backend configuration")

add_subdirectory(src)
