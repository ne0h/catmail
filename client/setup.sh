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

# build thrift
if [ ! -d thrift-build ]; then
	cd thrift
	./bootstrap.sh

	thriftopts="--prefix=$pwdstr/../3rdparty/thrift-build \
			--with-python --without-c_glib \
			--without-csharp --without-java --without-erlang --without-lua --without-perl --without-php \
			--without-php_extension --without-ruby --without-haskell --without-go --without-haxe --without-d"

	# OSX needs separate installed openssl (via brew...)
	if [[ "$unamestr" == 'Darwin' ]]; then
		thriftopts=$thriftopts" --with-openssl=/usr/local/opt/openssl"
	fi

	./configure $thriftopts
	make -j3
	make install
	cd ..
fi

# build pysodium
if [ ! -d pysodium-build ]; then
	cd pysodium
	pyversion=`python --version`
	export PYTHONPATH=$pwdstr/../3rdparty/pysodium-build/lib/python`echo $pyversion | cut -c8-10`/site-packages/
	mkdir -p $PYTHONPATH
	python setup.py build
	python setup.py install --prefix=$pwdstr/../3rdparty/pysodium-build
	cd ..
fi
