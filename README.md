# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

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
