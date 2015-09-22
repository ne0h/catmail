#!/bin/sh

# identify platform
unamestr=`uname`
pwdstr=`pwd`
cd ../3rdparty

# build libsodium
if [ ! -f libsodium.built ]; then
	cd libsodium/
	./autogen.sh

	if [[ "$unamestr" == 'Darwin' ]]; then
		./dist-build/osx.sh
	fi

	if [[ "$unamestr" == 'Linux' ]]; then
		export PREFIX="$(pwd)/libsodium-linux"
		mkdir $PREFIX
		./configure --enable-minimal --prefix="$PREFIX"
		make -j3 check && make -j3 install
		make distclean > /dev/null
	fi

	cd ..
	touch libsodium.built
fi

# build cppunit
if [ ! -f cppunitm.built ]; then
	cd cppunit/
	./autogen.sh
	./configure --prefix=`pwd`/lib
	make -j3
	make install
	cd ..
	touch cppunitm.built
fi

