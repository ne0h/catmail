# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

## Build

1. Run `git submodule update --init`
1. Build dependencies `./setup.sh`

## Run

### Client

* Application: Run `python3 main.py`
* Tests: Run `python3 test_crypto.py`

### Server

`cd server && node catmailserver.js`

## Dependencies

### Client
* Python 3
* PyQt5
* OpenSSL

### Server

* NodeJS

**OSX:** Use homebrew to install python 3.5, pyqt5 and openssl.
