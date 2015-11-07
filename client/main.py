import sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("/Users/ne0h/Projekte/catmail/3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("/Users/ne0h/Projekte/catmail/3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("/Users/ne0h/Projekte/catmail/client/api/protocol")
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.7-py" 
	+ curVersion + ".egg")

from catmailtypes import *
 
if __name__ == '__main__':
	CatMailClient()