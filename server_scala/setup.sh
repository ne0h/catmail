#!/bin/sh

PROJECTS=("catmailapi" "catmailserver")

echo "Building API..."
OUTPUT="catmailapi/src"
rm -rf ${OUTPUT}
mkdir -p ${OUTPUT}
thrift -out ${OUTPUT} -r --gen java ../common/protocol.thrift

echo "Generating Eclipse project settings..."
for i in "${PROJECTS[@]}"
do
	cd $i
	gradle eclipse
	cd ..
done
