# CatMail

Cryptographic draft is available here: https://docs.google.com/document/d/124mqAbgqR8MiiCAtPnxXrI_gbZv6ZQbM6ahiNCEVEgs/edit?usp=sharing

## Build

Run `git submodule update --init`

### Client

#### Dependencies

* Python 3
* PyQt5
* OpenSSL

**OSX: ** Use homebrew to install python 3.5, pyqt5 and openssl.

#### Build & Run

1. `cd client`
1. Build dependencies: `./setup.sh`
2. Build api: `./buildapi.sh`
2. Run `python main.py`

#### Run Tests

Run `python test_crypto.py`