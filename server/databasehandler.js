var CatMailTypes = require("./api/protocol_types"),
	
	sqlite3      = require("sqlite3").verbose(),
 	db           = new sqlite3.Database("catmail.db");

function DatabaseHandler() {

	this.validatePasswordLogin = function(username, password, callback) {
		db.each("SELECT EXISTS (SELECT username, password FROM users WHERE username=? AND password=?) AS result;",
				{1: username, 2: password}, function(err, result) {
			(err) ? callback(err, null) : callback(null, result.result)
		});
	}

	this.getPrivateKeys = function(username, callback) {
		var sql = "SELECT `userkeypair_sk`, `userkeypair_pk`, `userkeypair_nonce`, `exchangekeypair_sk`, "
			+ "`exchangekeypair_pk`, `exchangekeypair_nonce` FROM `users` WHERE `username`=?;"
		db.each(sql, {1: username}, function(err, result) {
			if (err) {callback(err, null)}

			var userKeyPair = new CatMailTypes.EncryptedKeyPair();
			userKeyPair.encryptedSecretKey = result.userkeypair_sk;
			userKeyPair.nonce = result.userkeypair_nonce;
			userKeyPair.publicKey = result.userkeypair_pk;

			var exchangeKeyPair = new CatMailTypes.EncryptedKeyPair();
			exchangeKeyPair.encryptedSecretKey = result.exchangekeypair_sk;
			exchangeKeyPair.nonce = result.exchangekeypair_nonce;
			exchangeKeyPair.publicKey = result.exchangekeypair_pk;

			var response = new CatMailTypes.GetPrivateKeysResponse();
			response.userKeyPair = userKeyPair;
			response.exchangeKeyPair = exchangeKeyPair;

			callback(null, response);
		})
	}

}

module.exports = DatabaseHandler;
