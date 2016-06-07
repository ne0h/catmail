var CatMailTypes = require("./api/protocol_types"),

	async        = require("async"),
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

	/**
	 * Checks if a user exists or not.
	 * @param username the name of the user
	 * @param conn connection from mysql pool
	 * @param callback callback
     */
	function existsUser(username, conn, callback) {
		var sql = "SELECT EXISTS (SELECT `username` FROM `users` WHERE `username`=?) AS result;";
		conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error("Failed to check if a user called '" + username + "' already exists");
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, (result[0].result == 1));
		});
	}

	/**
	 * Checks if a contact has already been added to a contact list.
	 * @param username the name of the user who owns the contact list
	 * @param contactname the name of the user to check
	 * @param conn connection from mysql pool
	 * @param callback callback
     */
	function hasContact(username, contactname, conn, callback) {
		var sql = "SELECT EXISTS (SELECT `username`, `contactname` FROM `contacts` WHERE `username`=? AND"
				+ " `contactname`=?) AS result";
		conn.query(sql, [username, contactname], function(err, result) {
			if (err) {
				Logger.error("Failed to validate password for '" + username + "': " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, result[0].result == 1);
		});
	}

	/**
	 * Removes a user from all contact lists.
	 * @param username the name of the user to remove
	 * @param connection from the mysql pool
	 * @param callback callback
     */
	function removeFromAllContactLists(username, conn, callback) {
		var sql = "DELETE FROM `contacts` WHERE `contactname` LIKE ?";
		conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error("Failed to remove '" + username + "' from all contact lists: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, null);
		});
	}

	function existsChat(chatId, conn, callback) {
		var sql = "SELECT EXISTS (SELECT `id` FROM `chats` WHERE `id`=?) AS result";
		conn.query(sql, [chatId], function(err, result) {
			if (err) {
				Logger.error("Failed to validate that chat #" + chatId + " exists: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, result[0].result == 1);
		});
	}

	function isChatMember(username, chatId, conn, callback) {
		var sql = "SELECT EXISTS (SELECT `username`,`id` FROM `chatmembers` WHERE `username`=? AND `id`=?) AS result";
		conn.query(sql, [username, chatId], function(err, result) {
			if (err) {
				Logger.error("Failed to validate the user named '" + username + "' is in chat #" + chatId + ": "
					+ err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, result[0].result == 1);
		});
	}

	this.validatePasswordLogin = function(username, password, callback) {	
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
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
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
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
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
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
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
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

	this.addToContactList = function(username, userToAdd, attributes, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					conn.release();
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// make sure that the user to add exists
				existsUser(username, conn, function(err, result) {
					if (err) {
						conn.relase();
						callback(err, null);
						return;
					}

					if (result) {
						conn.release();
						Logger.info("Failed to create new user called '" + username + "': Username already taken");
						callback(new CatMailTypes.UserAlreadyExistsException(), null);
						return;
					}

					// Check if this contact has already been added
					hasContact(username, userToAdd, conn, function(err, result) {
						if (err) {
							conn.relase();
							callback(err, null);
							return;
						}

						if (result) {
							conn.release();
							callback(new CatMailTypes.ContactAlreadyExistsException(), null);
							return;
						}

						// get current contactlist version
						var sql = "SELECT `version` FROM `contacts` WHERE `username`=? ORDER BY `version` DESC LIMIT 1;";
						conn.query(sql, [username], function (err, result) {
							if (err) {
								conn.release();
								Logger.error("Failed to get current contactlist version count for user "
									+ username + ": " + err.stack);
								callback(new CatMailTypes.InternalException(), null);
								return;
							}

							newVersion = result[0].version + 1;

							sql = "INSERT INTO `contacts` SET ?;";
							conn.query(sql, [{
								"username": username, "contactname": userToAdd, "version": newVersion,
								"type": 0
							}], function (err, result) {

								if (err) {
									conn.release();
									Logger.error("Failed to add contact " + userToAdd + " to " + username
										+ "'s contactlist" + ": " + err.stack);
									callback(new CatMailTypes.InternalException(), null);
									return;
								}

								conn.commit(function (err) {
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
			});
		});
	}

	this.removeFromContactList = function(username, userToDelete, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					conn.release();
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// make sure that the user exists
				existsUser(username, conn, function(err, data) {
					if (err) {
						conn.relase();
						callback(err, null);
						return;
					}

					if (result) {
						conn.release();
						Logger.info("Failed to create new user called '" + username + "': Username already taken");
						callback(new CatMailTypes.UserAlreadyExistsException(), null);
						return;
					}

					// get current contactlist version
					var sql = "SELECT `version` FROM `contacts` WHERE `username`=? ORDER BY `version` DESC LIMIT 1;";
					conn.query(sql, [username], function(err, result) {
						if (err) {
							conn.release();
							Logger.error("Failed to get current contactlist version count for user " + username + ": "
								+ err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						newVersion = result[0].version + 1;

						sql = "UPDATE `contacts` SET `version`=?, `type`=? WHERE `username`=? AND `contactname`?;";
						conn.query(sql, [newVersion, 2, username, userToDelete], function(err, result) {
							if (err) {
								conn.release();
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
		});	
	}

	this.createUser = function(username, password, userKeyPair, exchangeKeyPair, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					conn.release();
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// make sure that the user does not exist
				existsUser(username, conn, function(err, result) {
					if (err) {
						conn.relase();
						callback(err, null);
						return;
					}

					if (result) {
						conn.release();
						Logger.info("Failed to create new user called '" + username + "': Username already taken");
						callback(new CatMailTypes.UserAlreadyExistsException(), null);
						return;
					}

					var userData = {};
					userData["username"] = username;
					userData["password"] = password;
					userData["userkeypair_sk"] = userKeyPair.encryptedSecretKey;
					userData["userkeypair_pk"] = userKeyPair.publicKey;
					userData["userkeypair_nonce"] = userKeyPair.nonce;
					userData["exchangekeypair_sk"] = exchangeKeyPair.encryptedSecretKey;
					userData["exchangekeypair_pk"] = exchangeKeyPair.publicKey;
					userData["exchangekeypair_nonce"] = exchangeKeyPair.nonce;

					var sql = "INSERT INTO `users` SET ?;";
					conn.query(sql, [userData], function (err, result) {
						conn.release();

						if (err) {
							Logger.error("Failed to add new user called '" + username + "': " + err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						} else {
							callback(null, null);
							return;
						}
					});
				});
			});
		});
	}

	/**
	 * Returns the list of chats of a given user.
	 * @param username the name of the user
	 * @param conn the mysql connection object
	 * @param callback is called when the method finishes
     */
	function getChats(username, conn, callback) {
		var sql = "SELECT `chatid` FROM chatmembers WHERE `username` LIKE ?;";
		conn.query(sql, [username], function(err, result) {
			if (err) {
				Logger.error("Failed to get chat list of '" + username + "'");
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			callback(null, result);
		});
	}

	this.deleteUser = function(username, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			// delete from chats
			var sql = "DELETE FROM `chatmembers` WHERE `username` LIKE ?;";
			conn.query(sql, [username], function(err, result) {
				if (err) {
					conn.release();
					Logger.error("Failed to delete chatmembers stuff for '" + username + "': " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// delete from contact lists
				sql = "DELETE FROM `contacts` WHERE `contactname` LIKE ?;";
				conn.query(sql, [username], function(err, result) {
					if (err) {
						conn.release();
						Logger.error("Failed to delete '" + username + "' from all other contactlists: " + err.stack);
						callback(new CatMailTypes.InternalException(), null);
						return;
					}

					sql = "DELETE FROM `users` WHERE `username` LIKE ?;";
					conn.query(sql, [username], function(err, result) {
						if (err) {
							conn.release();
							Logger.error("Failed to delete '" + username + "': " + err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						callback(null, null);
					});
				});
			});

			// delete user data
			conn.release();
		});
	}

	this.createChat = function(callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			// use 'SET' when there is actually more data then just a chatId
			var sql = "INSERT INTO `chats` () VALUES ()";
			conn.query(sql, [], function(err, result) {
				conn.release();

				if (err) {
					Logger.error("Failed to create chat: " + err.stack);
					callback(new CatMailTypes.InternalException(), null)
				} else {
					Logger.debug("New chat with id " + result.insertId);
					callback(null, result.insertId);
				}
			});
		});
	}

	this.addUsersToChat = function(chatId, users, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function(err) {
				if (err) {
					conn.release();
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// check if all the users exist
				var sql = "SELECT `username` FROM `users` where `username` IN (";
				for (var i = 0; i < users.length; i++) {
					sql += "'" + users[i].username + "',"
				}
				sql = sql.substring(0, sql.length - 1);
				sql += ");";
				conn.query(sql, [], function(err, result) {
					if (err) {
						conn.release();
						Logging.error("Failed to check if the users exist: " + err.stack);
						callback(new CatMailTypes.InternalException(), null);
						return;
					}

					// iterate the result to check if the users exist
					brokenUsers = [];
					var values = "";
					for (var i = 0; i < users.length; i++) {
						if (result.indexOf(users[i].username) == -1) {
							brokenUsers.push(users[i].username);
						} else {
							values += "('" + users[i].username + "','" + chatId + "','" + users[i].key + "'),"
						}
					}
					values = values.substring(0, values.length - 1);

					// insert all the users
					sql = "INSERT INTO `users` (`username`,`chatid`,`userkey`) VALUES " + values + ";";
					conn.query(sql, [], function(err, result) {
						conn.release();

						if (err) {
							Logging.error("Failed to add users to chat #: " + chatId + " | " + err.stack);
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						if (brokenUsers.length > 0) {
							callback(new CatMailTypes.UserDoesNotExistException(brokenUsers),
								new CatMailTypes.CreateChatResponse(chatId));
						} else {
							callback(null, new CatMailTypes.CreateChatResponse(chatId));
						}
					});
				});
			});
		});
	}

	function addSingleUserToChat(username, chatId, key, conn, callback) {
		existsUser(username, conn, function(err, result) {
			if (err) {
				callback(err);
				return;
			}

			if (!result) {
				Logger.error("'" + username + "' does not exist");
				callback(new CatMailTypes.UserDoesNotExistException([username]));
				return;
			}

			isChatMember(username, chatId, conn, function(err, result) {
				if (err) {
					callback(err);
					return;
				}

				if (!result) {
					Logger.error("'" + username + "' is already chat member");
					callback(new CatMailTypes.UserDoesNotExistException([username]));
					return;
				}

				var sql = "INSERT INTO `chatmembers` SET ?;";
				conn.query(sql, [{
					"username": username, "chatid": chatId, "userkey": key
				}], function(err, result) {
					if (err) {
						Logger.error("Failed to add userdata to chatmember table");
						callback(new CatMailTypes.InternalException());
						return;
					}

					callback();
				});
			})
		});
	}

	this.addToChat = function(username, chatId, usersToAdd, callback) {
		pool.getConnection(function(err, conn) {
			if (err) {
				conn.release();
				Logger.error("Failed to get mysql connection from pool: " + err.stack);
				callback(new CatMailTypes.InternalException(), null);
				return;
			}

			conn.beginTransaction(function (err) {
				if (err) {
					conn.release();
					Logger.error("Failed to start transaction: " + err.stack);
					callback(new CatMailTypes.InternalException(), null);
					return;
				}

				// look if the chat exists
				existsChat(chatId, conn, function(err, result) {
					if (err) {
						conn.relase();
						callback(err, null);
						return;
					}

					if (!result) {
						conn.release();
						Logger.info("Failed to add users to chat: Chat with id #" + chatId + " does not exist.");
						callback(new CatMailTypes.ChatDoesNotExistException(), null);
						return;
					}

					// check if the current user is in this chat
					isChatMember(username, chatId, conn, function(err, result) {
						if (err) {
							conn.relase();
							callback(err, null);
							return;
						}

						if (!result) {
							conn.release();
							Logger.info("Failed to add users to chat: User named '" + username + "' is not member.");
							callback(new CatMailTypes.InternalException(), null);
							return;
						}

						// add every user to chat...
						async.each(usersToAdd, function(user, callback) {
							Logger.debug("Adding '" + user.username + "' to chat #" + chatId + "...");
							addSingleUserToChat(user.username, chatId, user.key, conn, function(err) {
								(err) ? callback(err) : callback()
							});
						}, function(err) {
							if (err) {
								Logger.error("Failed to add all users to chat #" + chatId);
								conn.release();
								callback(err, null);
								return;
							}

							callback(null, null);
						});
					});
				});
			});
		});
	}

}

module.exports = DatabaseHandler;
