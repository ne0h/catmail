var CatMailTypes	= require("./api/protocol_types"),
	
	DatabaseHandler = require("./databasehandler"),
	databaseHandler = new DatabaseHandler(),

	CryptoHelper    = require("./cryptohelper"),
	cryptoHelper    = new CryptoHelper();

function ClientHandler() {

	this.getPrivateKeys = function(username, password, callback) {
		databaseHandler.validatePasswordLogin(username, cryptoHelper.sha256(password), function(err, result) {
			if (err) {callback(new CatMailTypes.InternalException())}
			if (result == 0) {callback(new CatMailTypes.InvalidLoginCredentialsException())}

			databaseHandler.getPrivateKeys(username, function(err, result) {
				if (err) {callback(new CatMailTypes.InternalException())}
				callback(null, result);
			});
		});
	}

	this.login = function(username, password, callback) {
		callback(null, null);
	}

	this.logout = function(username, password, callback) {
		callback(null, null);
	}

	this.createUser = function(username, password, userKeyPair, exchangeKeyPair, callback) {
		callback(null, null);
	}

}

module.exports = ClientHandler;
