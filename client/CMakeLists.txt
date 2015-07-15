cmake_minimum_required(VERSION 2.8)

project("catmail-client")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    include_directories(/usr/local/include ../3rdparty/libsodium/libsodium-osx/include)
    link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-osx/lib/)
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    include_directories(../3rdparty/libsodium/libsodium-linux/include)
    link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-linux/lib/)    
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")

add_executable(catmail-client main.cpp keypair.cpp cryptohelper.cpp user.cpp contact.cpp)
target_link_libraries(catmail-client sodium)
