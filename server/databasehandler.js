var CatMailTypes = require("./api/protocol_types"),
	
	mysql        = require("mysql"),
	Log4js       = require("log4js"),
	Logger       = Log4js.getLogger("databasehandler");

function DatabaseHandler(settings) {

	var that = this;

	var pool = mysql.createPool({
		host:     settings.hostname,
		user:     settings.username,
		password: settings.password,
		database: settings.database
	});

	this.validatePasswordLogin = function(username, password, callback) {
		
		var sql = "SELECT EXISTS (SELECT `username`, `password` FROM users WHERE `username`=? AND `password`=?)"
			+ " AS result;";
		
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.query(sql, [username, password], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to validate password for " + username + ": " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				} else {
					callback(null, result[0].result)}
			});
		});
	}

	this.getPrivateKeys = function(username, callback) {

		var sql = "SELECT `userkeypair_sk`, `userkeypair_pk`, `userkeypair_nonce`, `exchangekeypair_sk`,"
			+ " `exchangekeypair_pk`, `exchangekeypair_nonce` FROM `users` WHERE `username`=?;";

		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.query(sql, [username], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get private keys for " + username + ": " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

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
		});
	}

	this.createUser = function(username, userKeyPair, exchangeKeyPair, callback) {
		//First check if username already exists
		var sql = "SELECT EXISTS( SELECT `username` FROM `users` WHERE `username`=? AS user_exists;";
		//SELECT EXISTS(SELECT username FROM catmail.users WHERE username='benjamin@catmail.de') AS result;
		this.conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error("Faild to check if username " + username + "exists: " + err.stack);
				callback(err, null);
				return;
			} else {
				if (result[0].user_exists) {
					Logger.inform("A user with username: " + username + " already exists");
					callback(err, null);
					return;
				} else {
					this.conn.query("INSERT INTO `users`SET ?;",[{"username":username, 
						"userkeypair_pk":userKeyPair.userkeypair_pk, "userkeypair_nonce":userKeyPair.userkeypair_nonce, 
						"userkeypair_sk":userKeyPair.userkeypair_sk, "exchangekeypair_pk":exchangeKeyPair.exchangekeypair_pk,
						"exchangekeypair_nonce":exchangeKeyPair.exchangekeypair_nonce, 
						"exchangeKeyPair":exchangeKeyPair.exchangekeypair_sk}], function(err, result){
							if (err) { 
								Logger.error("Adding user with username: " + username +" failed " + err.stack);
								callback(err, null);
								return;
							}
						});
				}
			}
		})
	}

	this.getExchangeKeyPairPublicKey = function(username, callback) {

		var sql = "SELECT `exchangekeypair_pk` FROM `users` WHERE `username`=?;";

		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.query(sql, [username], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get exchange keypair for " + username + ": " + err.stack);
					callback(err, null);
					return;
				}

				callback(null, result[0].exchangekeypair_pk);
			});
		});
	}

	this.getContactList = function(username, version, callback) {

		var sql = "SELECT `contactname` FROM `contacts` WHERE `username`=? AND version>?;";

		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.query(sql, [username, version], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get contactlist for " + username + ": " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				var response = new CatMailTypes.GetContactListResponse();
				response.contacts = [];

				for (var i in result) {response.contacts.push(new CatMailTypes.Contact(result[i].contactname), {});}

				callback(null, response);
			});
		});
	}

	this.addToContactList = function(username, userToAdd, attributes, callback) {
			
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					Logger.error("Failed to add " + userToAdd + " to contact list of " + username + " " + err.stack)
					callback(new CatMailTypes.InternalException(), null);
					return;
				}
				
				var sql = "UPDATE `users` SET `contacts_version`=`contacts_version`+1 WHERE `username`=?;";
				conn.query(sql, [username], function(err, result) {
					if (err) {
						return that.conn.rollback(function() {
							Logger.error("Failed to add " + userToAdd + " to contact list of " + username + " " + err.stack)
							callback(err, null);
							return;
						});
					}

				sql = "SELECT `contacts_version` FROM `users` WHERE `username`=?;";
				conn.query(sql, [username], function(err, result) {
						if (err) {
							return that.conn.rollback(function() {
								Logger.error("Failed to add " + userToAdd + " to contact list of " + username + " "
									+ err.stack)
								callback(err, null);
								return;
							});
						}
				
						var version = result[0].contacts_version;

						sql = "INSERT INTO `contacts` SET ?;";
						conn.query(sql, [{"username": username, "contactname": userToAdd,
								"version": version}], function(err, result) {
							if (err) {
								return that.conn.rollback(function() {
									Logger.error("Failed to add " + userToAdd + " to contact list of " + username + " "
										+ err.stack)
									callback(err, null);
									return;
								});
							}

							conn.commit(function(err) {
								conn.release();
								if (err) {
									return that.conn.rollback(function() {
										Logger.error("Failed to add " + userToAdd + " to contact list of " + username + " "
											+ err.stack)
										callback(err, null);
										return;
									});
								}

								var response = new CatMailTypes.AddToContactListResponse();
								response.version = version;

								callback(null, response);
							});
						})
					});
				});
			});
		});
	}

}

module.exports = DatabaseHandler;
