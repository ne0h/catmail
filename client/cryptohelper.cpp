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

std::string CryptoHelper::encode(std::string message, std::string iv, std::string recipientPublicKey,
		std::string senderPrivateKey) {

	unsigned char c[4096];
	crypto_box_easy(c, (const unsigned char*) message.c_str(), message.size(), (const unsigned char*) iv.c_str(),
		(const unsigned char*) recipientPublicKey.c_str(), (const unsigned char*) senderPrivateKey.c_str());

	std::string result((char*) c);
	return result;
}