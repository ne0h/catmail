#!/bin/sh
rm -rf api
mkdir api
thrift -out api -r --gen py ../common/protocol.thrift
cd api/protocol
echo "import sys\nsys.path.append('../3rdparty/thrift-build/lib/python2.7/site-packages/thrift.egg')\n\n$(cat CatMailService.py)" > CatMailService.py
