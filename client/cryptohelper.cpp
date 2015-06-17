#include "cryptohelper.hpp"

CryptoHelper::CryptoHelper() {
	sodium_init();
}

KeyPair CryptoHelper::generateKeyPair() {
	
	unsigned char sk[crypto_box_SECRETKEYBYTES];
	unsigned char pk[crypto_box_PUBLICKEYBYTES];
	crypto_box_keypair(pk, sk);
	
	std::string privateKey((char*) sk);
	std::string publicKey((char*) pk);

	return KeyPair(privateKey, publicKey);
}

std::string CryptoHelper::encodeAsym(std::string message, std::string nonce, std::string recipientPublicKey,
		std::string senderPrivateKey) {
	
	unsigned char cypherText[message.size()];
	if (crypto_box_easy(cypherText, (const unsigned char*) message.c_str(), message.size(),
			(const unsigned char*) nonce.c_str(), (const unsigned char*) recipientPublicKey.c_str(),
			(const unsigned char*) senderPrivateKey.c_str()) != 0) {

		std::cout << "error while encoding" << std::endl;
	}

	std::string result((char*) cypherText);
	return result;
}

std::string CryptoHelper::decodeAsym(std::string cypherText, std::string nonce, std::string recipientPrivateKey,
		std::string senderPublicKey) {

	unsigned char message[cypherText.size()];
	if (crypto_box_open_easy(message, (const unsigned char*) cypherText.c_str(), cypherText.size(),
			(const unsigned char*) nonce.c_str(), (const unsigned char*) senderPublicKey.c_str(),
			(const unsigned char*) recipientPrivateKey.c_str()) != 0) {

		std::cout << "error while decoding" << std::endl;
	}

	std::string result((char*) message);
	return result;
}