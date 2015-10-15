#!/bin/sh
rm -rf api
mkdir api
thrift -out api -r --gen js:node ../common/protocol.thrift