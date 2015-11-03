import sys, glob, os
sys.path.append("api")
sys.path.insert(0, glob.glob("../3rdparty/thrift-build/lib/lib*")[0])
from protocol import CatMailService
from protocol.ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol

try:
	transport = THttpClient.THttpClient("http://localhost:9000/catmail")
	transport = TTransport.TBufferedTransport(transport)
	protocol = TJSONProtocol.TJSONProtocol(transport)

	client = CatMailService.Client(protocol)
	transport.open()

	client.login("me", "pw")

except Thrift.TException, tx:
	print '%s' % (tx.message)
