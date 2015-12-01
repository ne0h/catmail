var Thrift			= require("thrift"),
	CatMailService 	= require("./api/CatMailService"),
	CatMailTypes	= require("./api/protocol_types"),

	ClientHandler	= require("./clienthandler"),
	clientHandler	= new ClientHandler(),

	Log4js			= require("log4js"),
	Logger 			= Log4js.getLogger("catmailserver"),
	Getopt 			= require('node-getopt');

Log4js.configure('log_config.json', {cwd : 'logs'});

// Getopt arguments options
// '=':   has argument
// '[=]': has argument but optional
// '+':   multiple option supported
getopt = new Getopt([
	['h', 'help', 'Display this help.'],
	['v', 'verbose', 'Print logging output on console (additional to log).'],
	['l', 'level=LEVEL', 'Debug log level']
]).bindHelp();

//Log4js.addAppender(Log4js.appenders.file("catmail.log"), "catmailserver");

var CatMailHandler = {

	createUser: function(username, userKeyPair, exchangeKeyPair, callback){
		clientHandler.createUser(username, userKeyPair, exchangeKeyPair,function(err, data){
			(!err) ? callback(null, data) : callback(err)
		});
	},

	getPrivateKeys: function(username, password, callback) {
		Logger.debug(username + " wants to download his secret keys")
		clientHandler.getPrivateKeys(username, password, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

	requestLoginChallenge: function(username, callback) {
		Logger.debug(username + " wants a challenge")
		clientHandler.requestLoginChallenge(username, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

	login: function(username, challenge, signature, callback) {
		Logger.debug(username + " wants to log in")
		clientHandler.login(username, challenge, signature, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

	logout: function(username, sessionToken, callback) {
		Logger.debug(username + " tries to log out")
		clientHandler.logout(username, sessionToken, function(err, data) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

	getContactList: function(username, sessionToken, version, callback) {
		Logger.debug(username + " wants to download his contact list")
		clientHandler.getContactList(username, sessionToken, version, function(err, result) {
			(!err) ? callback(null, result) : callback(err)
		});
	},

	addToContactList: function(username, sessionToken, userToAdd, attributes, callback) {
		Logger.debug(username + " to add " + userToAdd + " to his contact list")
		clientHandler.addToContactList(username, sessionToken, userToAdd, attributes, function(err, result) {
			(!err) ? callback(null, data) : callback(err)
		});
	},

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


function handle_cmd_args(options) {
	if (options.verbose) {
		Log4js.addAppender(Log4js.appenders.console());
	}
	if (options.level) {
		var level;
		switch (options.level.toUpperCase()) {
			case 'DEBUG':
				level = 'DEBUG'; break;
			case 'INFO':
				level = 'INFO'; break;
			case 'WARN':
				level = 'WARN'; break;
			case 'ERROR':
				level = 'ERROR'; break;
			case 'FATAL':
				level = 'FATAL'; break;
			default:
				console.error('Got invalid log level.'
					+ 'Valid values are debug, info, warn error or fatal.'
				);
			process.exit(1);
		}
		Logger.setLevel(level);
	}
}

handle_cmd_args(getopt.parse(process.argv.slice(2)).options);

var server = Thrift.createWebServer(serverOpt);
server.on('error', function(err) {
	Logger.error("Thrift WebServer Error: " + err);
});
server.listen(9000);
Logger.info("CatMail Server up and running...");
