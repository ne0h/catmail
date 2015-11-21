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

	this.validateSignature = function(challenge, signature, publicKey) {
		var result = sodium.crypto_sign_open(new Buffer(signature, "base64"), new Buffer(publicKey, "base64"));
		return (new Buffer(result, "utf-8").toString() == challenge)
	}

	// Math.random in V8 is baaaaad
	// http://www.heise.de/newsticker/meldung/JavaScript-Engine-V8-Vorsicht-vor-Math-random-3010353.html
	this.randomId = function() {
		var nonce = new Buffer(16);
		sodium.randombytes_buf(nonce);

		var result = "";
		for (var i = 0; i < nonce.length; i++) {
			var c = nonce[i].toString(16);
			if (c.length == 1) {c = "0" + c;}
			result += c;
		}

		return result;
	}

}

module.exports = CryptoHelper;
