#!/bin/sh
rm -rf api
mkdir api
../3rdparty/thrift-build/bin/thrift -out api -r --gen js:node ../common/protocol.thrift