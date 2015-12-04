var CatMailTypes	= require("./api/protocol_types"),
	
	Config          = require("./config"),
	DatabaseHandler = require("./databasehandler"),
	databaseHandler = new DatabaseHandler(Config.database),
	CryptoHelper    = require("./cryptohelper"),
	cryptoHelper    = new CryptoHelper(),

	Log4js = require("log4js"),
	Logger = Log4js.getLogger("catmailserver");

function ClientHandler() {

	that = this;

	/**
	 * Contains a list of active sessions for each user.
	 * Map<username, sessionTokens[]>
	 */
	var sessions   = {}

	/**
	 * Adds a new session for a user.
	 */
	function addSession(username, sessionToken) {
		if (!sessions[username]) {sessions[username] = []}
		sessions[username].push(sessionToken)
	}

	/**
	 * Removes an active session for a user.
	 */
	function removeSession(username, sessionToken) {
		sessions[username].splice(sessions[username].indexOf(sessionToken))
	}

	/**
	 * Validates if a session is valid.
	 */
	function validateSession(username, sessionToken, callback) {
		(sessions[username].indexOf(sessionToken) != -1) ? callback(true) : callback(false)
	}

	/**
	 * Contains a list of challenges for each user.
	 * Map<username, challenge[]>
	 */
	var challenges = {}

	/**
	 * Adds a new challenge.
	 */
	function addChallenge(username, challenge) {
		challenges[challenge] = username;
	}

	/**
	 * Removes an existing challenge
	 */
	function removeChallenge(challenge) {
		delete challenges[challenge]
	}

	this.getPrivateKeys = function(username, password, callback) {
		Logger.debug(username + " wants to download his secret keys")
		databaseHandler.validatePasswordLogin(username, cryptoHelper.sha256(password), function(err, result) {
			if (err) {callback(new CatMailTypes.InternalException()); return;}
			if (result == 0) {callback(new CatMailTypes.InvalidLoginCredentialsException()); return;}

			databaseHandler.getPrivateKeys(username, function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException()) : callback(null, result);
			});
		});
	}

	this.requestLoginChallenge = function(username, callback) {
		Logger.debug(username + " wants a challenge");

		var challenge = cryptoHelper.randomId();
		addChallenge(username, challenge);

		var response = new CatMailTypes.RequestLoginChallengeResponse();
		response.challenge = challenge;
		callback(null, response);
	}

	this.login = function(username, challenge, signature, callback) {
		Logger.debug(username + " wants to log in")
		databaseHandler.getExchangeKeyPairPublicKey(username, function(err, result) {

			// TODO: use real hostname
			if (challenges[challenge] != username || !cryptoHelper.validateSignature(challenge + "/catmail.de",
					signature, result)) {
				callback(new CatMailTypes.InvalidLoginCredentialsException())
			} else {
				// generate session token
				var sessionToken = cryptoHelper.randomId();

				// add session
				addSession(username, sessionToken);

				// remove challenge
				removeChallenge(challenge);

				var response = new CatMailTypes.LoginResponse();
				response.sessionToken = sessionToken;
				Logger.info(username + " logged in");
				callback(null, response);
			}
		});
	}

	this.logout = function(username, sessionToken, callback) {
		Logger.debug(username + " tries to log out")
		validateSession(username, sessionToken, function(result) {
			removeSession(username, sessionToken);
			(result) ? callback(null, null)	: callback(new CatMailTypes.InvalidSessionException())
		});
	}

	this.createUser = function(username, userKeyPair, exchangeKeyPair, callback) {
		databaseHandler.createUser(username, userKeyPair, exchangeKeyPair, function(err, result) {
			
		});
	}

	this.getContactList = function(username, sessionToken, version, callback) {
		Logger.debug(username + " wants to download his contact list")
		validateSession(username, sessionToken, function(result) {
			if (!result) {callback(new CatMailTypes.InvalidSessionException()); return;}
			
			databaseHandler.getContactList(username, version, function(err, result) {
				(err) ? callback(new CatMailTypes.InternalException(), null) : callback(null, result)
			});
		});
	},

	this.addToContactList = function(username, sessionToken, userToAdd, attributes, callback) {
		Logger.debug(username + " to add " + userToAdd + " to his contact list")
		validateSession(username, sessionToken, function(result) {
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
