# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

## Build

Run `git submodule update --init`

### Client

#### Dependencies

* libjson-rpc-cpp

#### Build & Run

1. `cd client`
1. `./setup.sh`
1. `mkdir build && cd build`
2. `cmake ..`
3. `make`
4. `./catmail-client`

#### Run Tests

Run `./testrunner` to execute unit tests.
