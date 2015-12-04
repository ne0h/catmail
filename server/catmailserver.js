var Thrift			= require("thrift"),
	CatMailService 	= require("./api/CatMailService"),
	CatMailTypes	= require("./api/protocol_types"),

	ClientHandler	= require("./clienthandler"),
	clientHandler	= new ClientHandler(),

	Log4js			= require("log4js"),
	Logger 			= Log4js.getLogger("catmailserver"),
	Getopt 			= require('node-getopt');

Log4js.configure('log_config.json', {cwd : 'logs'});
//Log4js.addAppender(Log4js.appenders.file("catmail.log"), "catmailserver");

/*
 * Getopt arguments options:
 *  '=':   has argument
 * '[=]': has argument but optional
 *  '+':   multiple option supported
 */
getopt = new Getopt([
	["h", "help",        "Display this help."],
	["v", "verbose",     "Print logging output on console (additional to log)."],
	["l", "level=LEVEL", "Debug log level"]
]).bindHelp();

/**
 * This class implements the thrift handler that passes all queries to the catmail server.
 * Every query is handled in ClientHandler, CatMailHandler acts just as an interface.
 */
var CatMailHandler = {

	getPrivateKeys: function(username, password, callback) {
		clientHandler.getPrivateKeys(username, password, function(err, data) {
			callback(err, data)
		});
	},

	requestLoginChallenge: function(username, callback) {
		clientHandler.requestLoginChallenge(username, function(err, data) {
			callback(err, data)
		});
	},

	login: function(username, challenge, signature, callback) {
		clientHandler.login(username, challenge, signature, function(err, data) {
			callback(err, data)
		});
	},

	logout: function(username, sessionToken, callback) {
		clientHandler.logout(username, sessionToken, function(err, data) {
			callback(err, data)
		});
	},

	getContactList: function(username, sessionToken, version, callback) {
		clientHandler.getContactList(username, sessionToken, version, function(err, result) {
			callback(err, data)
		});
	},

	addToContactList: function(username, sessionToken, userToAdd, attributes, callback) {
		clientHandler.addToContactList(username, sessionToken, userToAdd, attributes, function(err, result) {
			callback(err, data)
		});
	},

	createUser: function(username, password, userKeyPair, exchangeKeyPair, callback) {
		clientHandler.createUser(username, password, userKeyPair, exchangeKeyPair,function(err, data) {
			callback(err, data)
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


function handleCmdArgs(options) {
	if (options.verbose) {Log4js.addAppender(Log4js.appenders.console());}
	if (options.level) {
		var level;
		switch (options.level.toUpperCase()) {
			case "DEBUG":
				level = "DEBUG"; break;
			case "INFO":
				level = "INFO"; break;
			case "WARN":
				level = "WARN"; break;
			case "ERROR":
				level = "ERROR"; break;
			case "FATAL":
				level = "FATAL"; break;
			default:
				console.error("Got invalid log level. Valid values are debug, info, warn error or fatal.");
			process.exit(1);
		}
		Logger.setLevel(level);
	}
}

handleCmdArgs(getopt.parse(process.argv.slice(2)).options);

var server = Thrift.createWebServer(serverOpt);
server.on("error", function(err) {
	Logger.error("Thrift WebServer Error: " + err);
});
server.listen(9000);
Logger.info("CatMail Server up and running...");
