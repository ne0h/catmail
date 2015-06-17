cmake_minimum_required(VERSION 2.8)

project("catmail-client")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    include_directories(/usr/local/include ../3rdparty/libsodium/libsodium-osx/include)
    link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-osx/lib/)
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

add_executable(catmail-client main.cpp keypair.cpp cryptohelper.cpp)
target_link_libraries(catmail-client sodium)
