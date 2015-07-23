#!/bin/sh
mkdir -p api
jsonrpcstub spec.json --cpp-client=ClientHandler
mv clienthandler.h api/clienthandler.hpp
