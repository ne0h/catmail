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

# build jsoncpp
cd jsoncpp
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=debug -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF -DARCHIVE_INSTALL_DIR=. -G "Unix Makefiles" ..
make
cd ../../

# build libjson-rpc-cpp
cd libjson-rpc-cpp
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=debug -DCOMPILE_TESTS=NO -DCOMPILE_EXAMPLES=NO -DHTTP_SERVER=NO -DUNIX_DOMAIN_SOCKET_SERVER=NO -DCMAKE_INSTALL_PREFIX="$pwdstr/../3rdparty/libjson-rpc-cpp/build" -JSONCPP_INCLUDE_PREFIX="../../jsoncpp/build/" ..
make
make install
cd ../../

# build api
cd ../client
mkdir -p api
if [[ "$unamestr" == 'Darwin' ]]; then
	export DYLD_LIBRARY_PATH="../3rdparty/libjson-rpc-cpp/build/lib"
fi

../3rdparty/libjson-rpc-cpp/build/bin/jsonrpcstub spec.json --cpp-client=ClientHandler
mv clienthandler.h api/clienthandler.hpp
