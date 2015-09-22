#!/bin/sh
OUTPUT="catmailapi/src"
rm -rf $OUTPUT
mkdir -p $OUTPUT
thrift -out $OUTPUT -r --gen java ../common/protocol.thrift
