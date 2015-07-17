#include "../include/cryptohelper.hpp"

CryptoHelper::CryptoHelper() {
	sodium_init();
}

KeyPair CryptoHelper::generateKeyPair() {
	
	unsigned char sk[crypto_box_SECRETKEYBYTES];
	unsigned char pk[crypto_box_PUBLICKEYBYTES];
	crypto_box_keypair(pk, sk);
	
	std::string secretKey((char*) sk, crypto_box_SECRETKEYBYTES);
	std::string publicKey((char*) pk, crypto_box_PUBLICKEYBYTES);

	return KeyPair(secretKey, publicKey);
}

Message CryptoHelper::encryptAsym(User *user, Contact *recipient, std::string message) {

	unsigned char nonce[crypto_box_NONCEBYTES];
	randombytes_buf(nonce, sizeof nonce);
	const unsigned int cipherLength = message.size() + crypto_box_MACBYTES;
	unsigned char cipherText[cipherLength];

	crypto_box_easy(cipherText, (const unsigned char *)message.c_str(), message.size(), nonce,
		(const unsigned char *)recipient->getUserPublicKey().c_str(),
		(const unsigned char *)user->getUserKeyPair()->getSecretKey().c_str());

	return Message(user->getUsername(), recipient->getUsername(), std::string((const char*)cipherText, cipherLength),
		std::string((const char*)nonce, crypto_box_NONCEBYTES));
}

std::string CryptoHelper::decryptAsym(User *user, Contact *sender, Message *message) {

	const unsigned int decryptLength = message->getMessage().size() - crypto_box_MACBYTES;
	unsigned char decrypted[decryptLength];

	return (crypto_box_open_easy(decrypted,
			(const unsigned char *)message->getMessage().c_str(),
			message->getMessage().size(),
			(const unsigned char *)message->getNonce().c_str(),
			(const unsigned char *)sender->getUserPublicKey().c_str(),
			(const unsigned char *)user->getUserKeyPair()->getSecretKey().c_str()) == 0)

		? std::string((const char*)decrypted, decryptLength) : "Fehler";
}