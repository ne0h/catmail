var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("catmail.db");

function DatabaseHandler() {

	this.validatePasswordLogin = function(username, password, callback) {
		db.each("SELECT EXISTS (SELECT username, password FROM users WHERE username=? AND password=?) AS result;",
				{1: username, 2: password}, function(err, result) {
			console.log(err + " " + result.result)
		});
	}

}

module.exports = DatabaseHandler;
