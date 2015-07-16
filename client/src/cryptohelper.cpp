#include "../include/cryptohelper.hpp"

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

Message CryptoHelper::encryptAsym(User *user, Contact *recipient, std::string message) {

	unsigned char nonce[crypto_box_NONCEBYTES];
	randombytes_buf(nonce, sizeof nonce);
	unsigned char cipherText[message.size() + crypto_box_MACBYTES];

	crypto_box_easy(cipherText, (const unsigned char *)message.c_str(), message.size(), nonce,
		(const unsigned char *)recipient->getUserPublicKey().c_str(),
		(const unsigned char *)user->getUserKeyPair()->getSecretKey().c_str());

	return Message(user->getUsername(), recipient->getUsername(), (const char*)cipherText,
		(const char*)nonce);
}

std::string CryptoHelper::decryptAsym(User *user, Contact *sender, Message *message) {

	unsigned char decrypted[message->getMessage().size() - crypto_box_MACBYTES];
	return (crypto_box_open_easy(decrypted,
			(const unsigned char *)message->getMessage().c_str(),
			message->getMessage().size(),
			(const unsigned char *)message->getNonce().c_str(),
			(const unsigned char *)sender->getUserPublicKey().c_str(),
			(const unsigned char *)user->getUserKeyPair()->getSecretKey().c_str()) == 0) ? (const char*)decrypted : "Fehler";
}