# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

## Build

Run `git submodule update --init`

### Client

#### Build & Run

1. `cd client`
1. `./setup.sh`
1. `mkdir build && cd build`
2. `cmake ..`
3. `make`
4. `DYLD_LIBRARY_PATH="../../3rdparty/libjson-rpc-cpp/build/lib" ./catmail-client`

#### Run Tests

Run `DYLD_LIBRARY_PATH="../../3rdparty/libjson-rpc-cpp/build/lib" ./testrunner` to execute unit tests.


## Server

### Requirements
python3
python-pip
sqlite3

Install flusk-JSONRPC via pip
sudo pip install Flask-JSONRPC

### RUN
python main.py
