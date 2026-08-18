cmake_minimum_required(VERSION 3.20)
project(PaideiaFSM LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_compile_options(-Wall -Wextra)

include_directories(include)
include_directories(external)

add_executable(fsm_engine src/main.cpp)