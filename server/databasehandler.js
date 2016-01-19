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

	var contactUpdateTypes = [];
	contactUpdateTypes.push(CatMailTypes.ContactUpdateType.CREATED);
	contactUpdateTypes.push(CatMailTypes.ContactUpdateType.DELETED);
	contactUpdateTypes.push(CatMailTypes.ContactUpdateType.UPDATED);

	this.validatePasswordLogin = function(username, password, callback) {	
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var sql = "SELECT EXISTS (SELECT `username`, `password` FROM users WHERE `username`=? AND `password`=?)"
				+ " AS result;";
			conn.query(sql, [username, password], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to validate password for '" + username + "': " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				} else {
					callback(null, result[0].result)}
			});
		});
	}

	this.getPrivateKeys = function(username, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var sql = "SELECT `userkeypair_sk`, `userkeypair_pk`, `userkeypair_nonce`, `exchangekeypair_sk`,"
				+ " `exchangekeypair_pk`, `exchangekeypair_nonce` FROM `users` WHERE `username`=?;";
			conn.query(sql, [username], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get private keys for '" + username + "': " + err.stack);
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

	this.getExchangeKeyPairPublicKey = function(username, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var sql = "SELECT `exchangekeypair_pk` FROM `users` WHERE `username`=?;";
			conn.query(sql, [username], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get exchange keypair for '" + username + "': " + err.stack);
					callback(err, null);
					return;
				}

				callback(null, result[0].exchangekeypair_pk);
			});
		});
	}

	this.getContactList = function(username, version, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var sql = "SELECT `contactname`, `type`, `version` FROM `contacts` WHERE `username`=? AND `version`>?"
						+ " ORDER BY `version` DESC;";
			conn.query(sql, [username, version], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to get contactlist for '" + username + "': " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				var response = new CatMailTypes.GetContactListResponse();
				response.version  = (result.length > 0) ? result[0].version : version;
				response.contactUpdates = [];

				for (var i in result) {
					var contactUpdate = new CatMailTypes.ContactUpdate();
					contactUpdate["contact"] = new CatMailTypes.Contact();

					contactUpdate["contact"]["username"] = result[i].contactname;
					contactUpdate["contact"]["attributes"] = {};
					contactUpdate["updateType"] = contactUpdateTypes[result[i].type];

					response.contactUpdates.push(contactUpdate);
				}

				callback(null, response);
			});
		});
	}

	this.hasContact = function(username, contactname, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var sql = "SELECT EXISTS (SELECT `username`, `contactname` FROM `contacts` WHERE `username`=? AND"
				+ " `contactname`=?) AS result";
			conn.query(sql, [username, contactname], function(err, result) {
				conn.release();
				if (err) {
					Logger.error("Failed to validate password for '" + username + "': " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				} else {
					callback(null, result[0].result)}
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
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// get current contactlist version
				var sql = "SELECT `version` FROM `contacts` WHERE `username`=? ORDER BY `version` DESC LIMIT 1;";
				conn.query(sql, [username], function(err, result) {
					if (err) {
						Logger.error("Failed to get current contactlist version count for user " + username + ": "
							+ err.stack);
						callback(new CatMailTypes.InternalException(), null);
						return;
					}

					newVersion = result[0].version + 1;

					sql = "INSERT INTO `contacts` SET ?;";
					conn.query(sql, [{"username": username, "contactname": userToAdd, "version": newVersion,
							"type": 0}], function(err, result) {

						if (err) {
							Logger.error("Failed to add contact " + userToAdd + " to " + username + "'s contactlist"
								+ ": " + err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						conn.commit(function(err) {
							conn.release();
							if (err) {
								Logger.error("Failed to commit transaction: " + err.stack);
								callback(new CatMailTypes.InternalException(), null);
								return;
							}

							var response = new CatMailTypes.AddToContactListResponse();
							response.version = newVersion;

							callback(null, response);
						});
					});
				});
			});
		});
	}

	this.removeFromContactList = function(username, userToDelete, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}
				
				// get current contactlist version
				var sql = "SELECT `version` FROM `contacts` WHERE `username`=? ORDER BY `version` DESC LIMIT 1;";
				conn.query(sql, [username], function(err, result) {
					if (err) {
						Logger.error("Failed to get current contactlist version count for user " + username + ": "
							+ err.stack);
						callback(new CatMailTypes.InternalException(), null);
						return;
					}

					newVersion = result[0].version + 1;

					sql = "UPDATE `contacts` SET `version`=?, `type`=? WHERE `username`=? AND `contactname`?;";
					conn.query(sql, [newVersion, 2, username, userToDelete], function(err, result) {
						if (err) {
							Logger.error("Failed to remove " + userToDelete + " from " + username + "'s contactlist: "
								+ err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						conn.commit(function(err) {
							conn.release();
							if (err) {
								Logger.error("Failed to commit transaction: " + err.stack);
								callback(new CatMailTypes.InternalException(), null);
								return;
							}

							var response = new CatMailTypes.RemoveFromContactListResponse();
							response.version = newVersion;

							callback(null, response);
						});
					});
				});
			});
		});	
	}

	this.existsUser = function(username, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}
			
			var sql = "SELECT EXISTS (SELECT `username` FROM `users` WHERE `username`=?) AS result;";
			conn.query(sql, [username], function(err, result) {
				if (err) {
					Logger.error("Failed to check if '" + username + "' already exists");
					callback(false);
					return;
				}

				callback(result[0].result);
			});
		});
	}

	this.createUser = function(username, password, userKeyPair, exchangeKeyPair, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				Logger.error("Failed to get mysql connection form pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			var userData = {};
			userData["username"] = username;
			userData["password"] = password;
			userData["userkeypair_sk"]    = userKeyPair.encryptedSecretKey;
			userData["userkeypair_pk"]    = userKeyPair.publicKey;
			userData["userkeypair_nonce"] = userKeyPair.nonce;
			userData["exchangekeypair_sk"]    = exchangeKeyPair.encryptedSecretKey;
			userData["exchangekeypair_pk"]    = exchangeKeyPair.publicKey;
			userData["exchangekeypair_nonce"] = exchangeKeyPair.nonce;
					
			var sql = "INSERT INTO `users` SET ?;";
			conn.query(sql, [userData], function(err, result) {
				if (err) { 
					Logger.error("Failed to add new user called '" + username + "': " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
				} else {
					callback(null, null);
				}
			});
		});
	}

}

module.exports = DatabaseHandler;
