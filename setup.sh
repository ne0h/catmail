#!/bin/sh

#
# COMMON STUFF
#

# identify platform
unamestr=`uname`
pwdstr=`pwd`
programs="thrift npm"

for p in $programs; do
    if ! hash $p 2>/dev/null; then
        echo "$p is not installed. Please install and re-run.";
        exit 1
    fi
done

cd 3rdparty

# OSX: use python3.5 from homebrew
pybin=python
if [[ "$unamestr" == 'Darwin' ]]; then
	pybin=/usr/local/bin/python3.5
fi

pyversion=`$pybin -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`

#
# build libsodium
#
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

#
# build thrift
#
if [ ! -d thrift-build ]; then
	cd thrift
	./bootstrap.sh

	thriftopts="--prefix=$pwdstr/3rdparty/thrift-build \
			--without-csharp --without-java --without-erlang --without-lua --without-perl --without-php \
			--without-php_extension --without-ruby --without-haskell --without-go --without-haxe --without-d \
			--without-c_glib --without-cpp"

	# OSX needs separate installed openssl (via brew...)
	if [[ "$unamestr" == 'Darwin' ]]; then
		thriftopts=$thriftopts" --with-openssl=/usr/local/opt/openssl"
	fi

	./configure $thriftopts
	make -j2
	make install

	# build python lib
	cd lib/py
	export PYTHONPATH=$pwdstr/3rdparty/thrift-build/lib/python$pyversion/site-packages/
	mkdir -p $PYTHONPATH
	$pybin setup.py build
	$pybin setup.py install --prefix=$pwdstr/3rdparty/thrift-build
	cd ../../../

	# symlink python lib to more practical name
	cd thrift-build/lib/python$pyversion/site-packages
	ln -sv thrift-* thrift.egg
	ln -sv six-* six.egg
	cd ../../../../
fi

#
# build pysodium
#
if [ ! -d pysodium-build ]; then
	cd pysodium
	export PYTHONPATH=$pwdstr/3rdparty/pysodium-build/lib/python$pyversion/site-packages/
	mkdir -p $PYTHONPATH
	$pybin setup.py build
	$pybin setup.py install --prefix=$pwdstr/3rdparty/pysodium-build
	cd ..
fi

#
# CLIENT STUFF
#

cd $pwdstr/client/
./buildapi.sh

#
# SERVER STUFF
#

# generate api
cd $pwdstr/server/
./buildapi.sh

# install nodejs dependencies
cd $pwdstr/server
npm install log4js mysql node-int64 q sodium node-getopt
