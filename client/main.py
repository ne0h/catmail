#!/usr/bin/env python2

import sys
sys.path.append("../3rdparty/pysodium-build/lib/python2.7/site-packages/pysodium-0.6.7-py2.7.egg")
import pysodium

pk, sk = pysodium.crypto_box_keypair()
print pk
