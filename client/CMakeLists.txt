cmake_minimum_required(VERSION 2.8)

PROJECT("catmail-client")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
FILE(GLOB SourceFiles RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "src/*.cpp")
LIST(REMOVE_ITEM SourceFiles "src/main.cpp")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    INCLUDE_DIRECTORIES(/usr/local/include ../3rdparty/libsodium/libsodium-osx/include)
    LINK_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-osx/lib/ ${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/cppunit/lib)
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    INCLUDE_DIRECTORIES(../3rdparty/libsodium/libsodium-linux/include)
    LINK_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-linux/lib/ ${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/cppunit/lib/lib)    
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")

INCLUDE_DIRECTORIES(../3rdparty/cppunit/lib/include)

ADD_EXECUTABLE(catmail-client src/main.cpp ${SourceFiles})
TARGET_LINK_LIBRARIES(catmail-client sodium)

FILE(GLOB UnitTests_SRCS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "tests/*Test.cpp" )
ADD_EXECUTABLE(testrunner tests/testrunner.cpp ${UnitTests_SRCS} ${SourceFiles})
TARGET_LINK_LIBRARIES(testrunner cppunit sodium)
FOREACH(test ${UnitTests_SRCS})
        GET_FILENAME_COMPONENT(TestName ${test} NAME_WE)
        ADD_TEST(${TestName} UnitTester ${TestName})
ENDFOREACH(test)

