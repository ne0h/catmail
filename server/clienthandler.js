var CatMailTypes	= require("./api/protocol_types"),
	
	Config          = require("./config"),
	DatabaseHandler = require("./databasehandler"),
	databaseHandler = new DatabaseHandler(Config.database),
	CryptoHelper    = require("./cryptohelper"),
	cryptoHelper    = new CryptoHelper(),

	Log4js = require("log4js"),
	Logger = Log4js.getLogger("catmailserver");

function ClientHandler() {

	function validateSessionToken(username, sessionToken, callback) {

	}

	that = this;

	var challenges = {}
	var sessions   = {}

	this.getPrivateKeys = function(username, password, callback) {
		databaseHandler.validatePasswordLogin(username, cryptoHelper.sha256(password), function(err, result) {
			if (err) {callback(new CatMailTypes.InternalException()); return;}
			if (result == 0) {callback(new CatMailTypes.InvalidLoginCredentialsException()); return;}

			databaseHandler.getPrivateKeys(username, function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException())
					: callback(null, result);
			});
		});
	}

	this.requestLoginChallenge = function(username, callback) {
		// TODO: use randombuf sodium function here
		var id = cryptoHelper.randomId();
		challenges[id] = username;

		var response = new CatMailTypes.RequestLoginChallengeResponse();
		response.challenge = id;
		callback(null, response);
	}

	this.login = function(username, challenge, signature, callback) {
		databaseHandler.getExchangeKeyPairPublicKey(username,
				function(err, result) {

			// TODO: use real hostname
			if (challenges[challenge] != username || !cryptoHelper.validateSignature(challenge + "/catmail.de",
					signature, result)) {
				callback(new CatMailTypes.InvalidLoginCredentialsException())
			} else {
				// generate session token
				var sessionToken = cryptoHelper.randomId();

				// add session
				if (!sessions[username]) {sessions[username] = []}
				sessions[username].push(sessionToken)

				var response = new CatMailTypes.LoginResponse();
				response.sessionToken = sessionToken;
				Logger.info(username + " logged in");
				callback(null, response);
			}
		});
	}

	this.logout = function(username, sessionToken, callback) {
		validateSessionToken(username, sessionToken, function(result) {
			(result) ? callback(null, null)	: callback(new CatMailTypes.InvalidSessionException())
		});
	}

	this.getContactList = function(username, sessionToken, version, callback) {
		validateSessionToken(username, sessionToken, function(result) {
			if (!result) {callback(new CatMailTypes.InvalidSessionException()); return;}

			databaseHandler.getContactList(username, version, function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException(), null) : callback(null, result)
			});
		});
	},

	this.addToContactList = function(username, sessionToken, userToAdd, attributes, callback) {
		validateSessionToken(username, sessionToken, function(result) {
			if (!result) {
				callback(new CatMailTypes.InvalidSessionException());
				return;
			}

			databaseHandler.addToContactList(username, userToAdd, attributes,
					function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException(), null) : callback(null, result)
			});
		});
	}

}

module.exports = ClientHandler;
