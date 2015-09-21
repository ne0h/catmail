#!/bin/sh
OUTPUT="docs/protocol"
rm -rf $OUTPUT
mkdir -p $OUTPUT
thrift -out $OUTPUT -r --gen html common/protocol.thrift
