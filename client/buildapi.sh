#!/bin/sh
rm -rf api
mkdir api
thrift -out api -r --gen py ../common/protocol.thrift
