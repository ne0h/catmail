var Thrift			= require("thrift"),
	CatMailService 	= require("./api/CatMailService"),
	CatMailTypes	= require("./api/protocol_types"),

	ClientHandler	= require("./clienthandler"),
	clientHandler	= new ClientHandler()

var CatMailHandler = {

	getPrivateKeys: function(username, password, callback) {
		console.log("Incoming query");
		clientHandler.getPrivateKeys(username, password, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	}

	/*logout: function(username, sessionToken, callback) {
		clientHandler.logout(username, sessionToken, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

	createUser: function(username, password, userKeyPair, exchangeKeyPair, callback) {
		clientHandler.createUser(username, password, userKeyPair, exchangeKeyPair, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	}*/

}

var serverOpt = {
	services: {
		"/catmail": {
			handler: CatMailHandler,
			processor: CatMailService,
			protocol: Thrift.TJSONProtocol,
			transport: Thrift.TBufferedTransport
		}
	}
};

var server = Thrift.createWebServer(serverOpt);
server.listen(9000);
