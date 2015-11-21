var CatMailTypes = require("./api/protocol_types"),
	
	mysql        = require("mysql");
	Log4js       = require("log4js"),
	Logger       = Log4js.getLogger("catmailserver");


function DatabaseHandler(settings) {

	this.conn = mysql.createConnection({
		host:     settings.hostname,
		user:     settings.username,
		password: settings.password,
		database: settings.database
	});

	this.conn.connect(function(err) {
		if (err) {
			Logger.error("Failed to connect to database server:" + err.stack);
			process.exit();
		} else {
			Logger.debug("Successfully connected to database server");
		}
	});

	this.validatePasswordLogin = function(username, password, callback) {
		var sql = "SELECT EXISTS (SELECT `username`, `password` FROM users"
			+ " WHERE `username`=? AND `password`=?) AS result;";
		this.conn.query(sql, [username, password], function(err, result) {
			if(err) {
				Logger.error('validatePasswordLogin: '+err.stack);
				callback(err, null);
			} else {
				callback(null, result[0].result)}
		});
	}

	this.getPrivateKeys = function(username, callback) {
		var sql = "SELECT `userkeypair_sk`, `userkeypair_pk`,"
			+ " `userkeypair_nonce`, `exchangekeypair_sk`,"
			+ " `exchangekeypair_pk`, `exchangekeypair_nonce` FROM `users`"
			+ " WHERE `username`=?;";
		this.conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error('getPrivateKeys: ' + err.stack);
				callback(err, null); return;}

			var userKeyPair = new CatMailTypes.EncryptedKeyPair();
			userKeyPair.encryptedSecretKey = result[0].userkeypair_sk;
			userKeyPair.nonce = result[0].userkeypair_nonce;
			userKeyPair.publicKey = result[0].userkeypair_pk;

			var exchangeKeyPair = new CatMailTypes.EncryptedKeyPair();
			exchangeKeyPair.encryptedSecretKey = result[0].exchangekeypair_sk;
			exchangeKeyPair.nonce = result[0].exchangekeypair_nonce;
			exchangeKeyPair.publicKey = result[0].exchangekeypair_pk;

			var response = new CatMailTypes.GetPrivateKeysResponse();
			response.userKeyPair = userKeyPair;
			response.exchangeKeyPair = exchangeKeyPair;

			callback(null, response);
		});
	}

	this.getExchangeKeyPairPublicKey = function(username, callback) {
		var sql = "SELECT `exchangekeypair_pk` FROM `users` "
			+ "WHERE `username`=?;";
		this.conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error('getExchangeKeyPairPublicKey: ' + err.stack);
				callback(err, null); return;
			}

			callback(null, result[0].exchangekeypair_pk);
		});
	}

	this.getContactList = function(username, version, callback) {
		var sql = "SELECT `contactname` FROM `contacts` WHERE `username`=?"
			+ " AND version>?;";
		this.conn.query(sql, [username, version], function(err, result) {
			if (err) {callback(err, null); return;}

			var response = new CatMailTypes.GetContactListResponse();
			response.contacts = [];

			for (var i in result) {response.contacts.push(
				new CatMailTypes.Contact(result[i].contactname), {});}

			callback(null, response);
		});
	}

	this.addToContactList = function(username, userToAdd, attributes,
			callback) {
		
	}

}

module.exports = DatabaseHandler;
