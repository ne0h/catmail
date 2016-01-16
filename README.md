# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

## Goals

* End-to-end encryption with transparent key management and synchronisation
* Multi device support with synchronized server based history (synchronization between all clients)
* Multi platform (Linux, OSX, Windows, iOS, Android,...)
* File transfer (pictures, ...), with optional server side storage (pictures are a part of the synchronized chat history)

## Build

1. Build submodules: `git submodule update --init`
1. Build dependencies: `./setup.sh`

## Run

### Client

* Application: `python3 main.py`
* UnitTests: `python3 test_crypto.py`

### Server

`node catmailserver.js`

## Dependencies

### Client
* Python 3
* PyQt5
* OpenSSL

### Server

* NodeJS

**OSX:** Use homebrew to install python 3.5, pyqt5 and openssl.
