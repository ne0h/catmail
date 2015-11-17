var DatabaseHandler = require("./databasehandler"),
	databaseHandler = new DatabaseHandler(),

	CryptoHelper    = require("./cryptohelper"),
	cryptoHelper    = new CryptoHelper();

function ClientHandler() {

	this.getPrivateKeys = function(username, password, callback) {
		console.log("starting");
		cryptoHelper.sha256(password, function(result) {
			databaseHandler.validatePasswordLogin(username, password, function(result) {
				console.log(validatePasswordLogin);
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
