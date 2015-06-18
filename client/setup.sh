#!/bin/bash

# identify platform
unamestr=`uname`


cd ../3rdparty/libsodium/
./autogen.sh

if [[ "$unamestr" == 'Darwin' ]]; then
	./dist-build/osx.sh
fi

if [[ "$unamestr" == 'Linux' ]] ; then
	export PREFIX="$(pwd)/libsodium-linux"
	mkdir $PREFIX
	./configure --enable-minimal --prefix="$PREFIX"
	make -j3 check && make -j3 install
	make distclean > /dev/null
fi