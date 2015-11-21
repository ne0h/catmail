var Thrift			= require("thrift"),
	CatMailService 	= require("./api/CatMailService"),
	CatMailTypes	= require("./api/protocol_types"),

	ClientHandler	= require("./clienthandler"),
	clientHandler	= new ClientHandler();

	var Log4js = require("log4js");
	Log4js.loadAppender('file');
	Log4js.addAppender(Log4js.appenders.file('catmail.log'),'catmailserver');
	var Logger = Log4js.getLogger('catmailserver');
	Logger.debug("test");


var CatMailHandler = {

	getPrivateKeys: function(username, password, callback) {
		clientHandler.getPrivateKeys(username, password, function(err, data) {
			if(err){
				Logger.error('getPrivateKeys: ' + err.stack);
				callback(err);
			} else {
				callback(null,data);
			}
		});
	},

	requestLoginChallenge: function(username, callback) {
		clientHandler.requestLoginChallenge(username, function(err, data) {
			if(err){
				Logger.error('requestLoginChallenge: ' + err.stack);
				callback(err);
			} else {
				callback(null,data);
			}
		});
	},

	login: function(username, challenge, signature, callback) {
		clientHandler.login(username, challenge, signature, function(err, data) {
			if(err){
				Logger.error('Login failer: ' + err.stack);
				callback(err)
			} else {
				Logger.debug(username + ' logged in');
				callback(null,data);
			}
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
