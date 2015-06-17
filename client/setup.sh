#!/bin/bash

# identify platform
unamestr=`uname`


cd ../3rdparty/libsodium/
./autogen.sh

if [[ "$unamestr" == 'Darwin' ]]; then
	./dist-build/osx.sh
fi

if [[ "$unamestr" == 'Linux' ]] ; then
	echo "Linux"
	cd dist-build
	make
fi
