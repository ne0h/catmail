#!/bin/bash

# identify platform
unamestr=`uname`


cd ../3rdparty/libsodium/
./autogen.sh

if [[ "$unamestr" == 'Darwin' ]]; then
	./dist-build/osx.sh
fi
