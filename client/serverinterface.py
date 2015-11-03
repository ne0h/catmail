import sys, glob, os
sys.path.append("api")
sys.path.insert(0, glob.glob("../3rdparty/thrift-build/lib/lib*")[0])
from protocol import CatMailService
from protocol.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol
