#include "cryptohelper.hpp"

CryptoHelper::CryptoHelper() {
	sodium_init();
}

KeyPair CryptoHelper::generateKeyPair() {
	
	unsigned char sk[crypto_box_SECRETKEYBYTES];
	unsigned char pk[crypto_box_PUBLICKEYBYTES];
	crypto_box_keypair(pk, sk);
	
	std::string secretKey((char*) sk);
	std::string publicKey((char*) pk);

	return KeyPair(secretKey, publicKey);
}

std::string CryptoHelper::encodeAsym(std::string message, std::string nonce, std::string recipientPublicKey,
		std::string senderSecretKey) {
	
	unsigned char cipherText[message.size() + crypto_box_MACBYTES];
	if (crypto_box_easy(cipherText, (const unsigned char*) message.c_str(), message.size(),
			(const unsigned char*) nonce.c_str(), (const unsigned char*) recipientPublicKey.c_str(),
			(const unsigned char*) senderSecretKey.c_str()) != 0) {

		std::cout << "error while encoding" << std::endl;
	}

	std::string result((char*) cipherText);
	return result;
}

std::string CryptoHelper::decodeAsym(std::string cypherText, std::string nonce, std::string recipientSecretKey,
		std::string senderPublicKey) {

	unsigned char message[cypherText.size() - crypto_box_MACBYTES];
	if (crypto_box_open_easy(message, (const unsigned char*) cypherText.c_str(), cypherText.size(),
			(const unsigned char*) nonce.c_str(), (const unsigned char*) senderPublicKey.c_str(),
			(const unsigned char*) recipientSecretKey.c_str()) != 0) {

		std::cout << "error while decoding" << std::endl;
	}

	std::string result((char*) message);
	return result;
}