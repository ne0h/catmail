var sodium = require("sodium").api;

function CryptoHelper() {

	this.sha256 = function(input) {
		var message = new Buffer(input, "utf-8");
		var hash = sodium.crypto_hash_sha256(message);

		var result = "";
		for (var b of hash) {
  			var c = b.toString(16);
  			if (c.length == 1) {c = "0" + c;}
  			result += c;
  		}

		return result;
	}

}

module.exports = CryptoHelper;
