var CatMailTypes	= require("./api/protocol_types"),
	
	Config          = require("./config"),
	DatabaseHandler = require("./databasehandler"),
	databaseHandler = new DatabaseHandler(Config.database),
	CryptoHelper    = require("./cryptohelper"),
	cryptoHelper    = new CryptoHelper();

	var Log4js = require("log4js");
	Log4js.loadAppender('file');
	Log4js.addAppender(Log4js.appenders.file('catmail.log'),'clienthandler');
	var Logger = Log4js.getLogger('clienthandler');
	Logger.debug("test");

function ClientHandler() {

	function randomId() {
		function block() {
			return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
		}
		var result = "";
		for (i = 0; i < 8; i++) {result += block();}
		return result;
	}

	that = this;

	var challenges = {}
	var sessions   = {}

	this.getPrivateKeys = function(username, password, callback) {
		databaseHandler.validatePasswordLogin(username, cryptoHelper.sha256(password), function(err, result) {
			if (err) {callback(new CatMailTypes.InternalException()); return;}
			if (result == 0) {callback(new CatMailTypes.InvalidLoginCredentialsException()); return;}

			databaseHandler.getPrivateKeys(username, function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException()) : callback(null, result);
			});
		});
	}

	this.requestLoginChallenge = function(username, callback) {
		// TODO: use randombuf sodium function here
		var id = randomId();
		challenges[id] = username;

		var response = new CatMailTypes.RequestLoginChallengeResponse();
		response.challenge = id;
		callback(null, response);
	}

	this.login = function(username, challenge, signature, callback) {
		databaseHandler.getExchangeKeyPairPublicKey(username, function(err, result) {
			// TODO: use real hostname
			if (challenges[challenge] != username || !cryptoHelper.validateSignature(challenge + "/catmail.de",
					signature, result))
				callback(new CatMailTypes.InvalidLoginCredentialsException())
			else {
				// generate session token
				var sessionToken = randomId();

				// add session
				if (!sessions[username])
					sessions[username] = []
				sessions[username].push(sessionToken)

				var response = new CatMailTypes.LoginResponse();
				response.sessionToken = sessionToken;
				callback(null, response);
			}
		});
	}

	this.logout = function(username, password, callback) {
		callback(null, null);
	}

	this.createUser = function(username, password, userKeyPair, exchangeKeyPair, callback) {
		callback(null, null);
	}

}

module.exports = ClientHandler;
