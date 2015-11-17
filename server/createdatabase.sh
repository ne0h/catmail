#!/bin/sh

DBFILE=catmail.db

if [ -f $DBFILE ]; then
	echo "Database exists."
	exit
fi

sqlite3 $DBFILE "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, userkeypair_sk TEXT, userkeypair_pk TEXT, userkeypair_nonce TEXT, exchangekeypair_sk TEXT, exchangekeypair_pk TEXT, exchangekeypair_nonce TEXT);"
