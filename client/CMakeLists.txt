cmake_minimum_required(VERSION 2.8)

PROJECT("catmail-client")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
SET(CMAKE_AUTOMOC ON)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)

INCLUDE_DIRECTORIES(
    include/
)

SET(SRCS
    src/base64.cpp
    src/contact.cpp
    src/cryptobox.cpp
    src/cryptohelper.cpp
    src/keypair.cpp
    src/message.cpp
    src/user.cpp
)

IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    INCLUDE_DIRECTORIES(/usr/local/include ../3rdparty/libsodium/libsodium-osx/include)
    LINK_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-osx/lib/ ${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/cppunit/lib)
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")

IF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    INCLUDE_DIRECTORIES(../3rdparty/libsodium/libsodium-linux/include)
    LINK_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/libsodium/libsodium-linux/lib/ ${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/cppunit/lib/lib)    
ENDIF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")

# QT5
FIND_PACKAGE(Qt5Core REQUIRED)
FIND_PACKAGE(Qt5Widgets REQUIRED)
FIND_PACKAGE(Qt5Gui REQUIRED)

SET(QT_SRCS
    src/firstrunwindow.cpp
    src/mainwindow.cpp
    src/newuserdialog.cpp
)

SET(UIS
    ui/firstrunwindow.ui
    ui/mainwindow.ui
    ui/newuserdialog.ui
)
QT5_WRAP_UI(UIS_H ${UIS})

SET(MUCS
    include/firstrunwindow.hpp
    include/mainwindow.hpp
    include/newuserdialog.hpp
)
QT5_WRAP_CPP(MUCS_HEADER ${MUCS})

# main application
ADD_EXECUTABLE(catmail-client
    src/main.cpp
    ${SRCS}
    ${QT_SRCS}
    ${UIS_H}
    ${MUCS_HEADER}
)
TARGET_LINK_LIBRARIES(catmail-client
    sodium
    Qt5::Widgets
)


# test runner

INCLUDE_DIRECTORIES(../3rdparty/cppunit/lib/include)

FILE(GLOB UnitTests_SRCS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "tests/*Test.cpp" )
ADD_EXECUTABLE(testrunner tests/testrunner.cpp ${UnitTests_SRCS} ${SRCS})
TARGET_LINK_LIBRARIES(testrunner cppunit sodium)
FOREACH(test ${UnitTests_SRCS})
        GET_FILENAME_COMPONENT(TestName ${test} NAME_WE)
        ADD_TEST(${TestName} UnitTester ${TestName})
ENDFOREACH(test)

