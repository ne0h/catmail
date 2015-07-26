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

Message CryptoHelper::encryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message) {

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

std::string CryptoHelper::decryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> sender,
		std::shared_ptr<Message> message) {

	const unsigned int decryptLength = message->getValue().size() - crypto_box_MACBYTES;
	unsigned char decrypted[decryptLength];

	return (crypto_box_open_easy(decrypted,
			(const unsigned char *)message->getValue().c_str(),
			message->getValue().size(),
			(const unsigned char *)message->getNonce().c_str(),
			(const unsigned char *)sender->getUserPublicKey().c_str(),
			(const unsigned char *)user->getUserKeyPair()->getSecretKey().c_str()) == 0)

		? std::string((const char*)decrypted, decryptLength) : "error";
}

std::string CryptoHelper::generateSymKey() {

	unsigned char key[crypto_secretbox_KEYBYTES];
	randombytes_buf(key, sizeof key);

	return std::string((const char*)key, crypto_secretbox_KEYBYTES);
}

std::string CryptoHelper::hash(std::shared_ptr<std::string> input) {

	char hash[crypto_pwhash_scryptsalsa208sha256_STRBYTES];
	crypto_pwhash_scryptsalsa208sha256_str(hash, (const char *)input->c_str(), input->size(),
		 crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_SENSITIVE, crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_SENSITIVE);

	return std::string((const char*)hash, crypto_pwhash_scryptsalsa208sha256_STRBYTES);
}

bool CryptoHelper::verifyHash(std::shared_ptr<std::string> input, std::shared_ptr<std::string> hash) {
	return (crypto_pwhash_scryptsalsa208sha256_str_verify((const char *)hash->c_str(),
														  (const char *)input->c_str(), input->size()) == 0);
}

CryptoBox CryptoHelper::encrypt(std::string message, std::string key) {

	unsigned char nonce[crypto_box_NONCEBYTES];
	randombytes_buf(nonce, sizeof nonce);

	const unsigned int cipherLength = crypto_secretbox_MACBYTES + message.size();
	unsigned char cipherText[cipherLength];

	crypto_secretbox_easy(cipherText, (const unsigned char *)message.c_str(), message.size(), nonce,
		(const unsigned char *)key.c_str());

	return CryptoBox(std::string((const char*)cipherText, cipherLength),
		std::string((const char*)nonce, crypto_box_NONCEBYTES));
}

Message CryptoHelper::encrypt(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message,
		std::string key) {

	CryptoBox encrypted = encrypt(message, key);
	return Message(user->getUsername(), recipient->getUsername(), encrypted.getValue(),
		encrypted.getNonce());
}

std::string CryptoHelper::decrypt(std::shared_ptr<CryptoBox> message, std::string key) {

	const unsigned int decryptLength = message->getValue().size() - crypto_secretbox_MACBYTES;
	unsigned char decrypted[decryptLength];

	return (crypto_secretbox_open_easy(decrypted,
			(const unsigned char *)message->getValue().c_str(),
			message->getValue().size(),
			(const unsigned char *)message->getNonce().c_str(),
			(const unsigned char *)key.c_str()) == 0) 
		? std::string((const char*)decrypted, decryptLength) : std::string("error");
}

std::string CryptoHelper::decrypt(std::shared_ptr<User> user, std::shared_ptr<Message> message, std::string key) {

	const unsigned int decryptLength = message->getValue().size() - crypto_secretbox_MACBYTES;
	unsigned char decrypted[decryptLength];

	return (crypto_secretbox_open_easy(decrypted,
			(const unsigned char *)message->getValue().c_str(),
			message->getValue().size(),
			(const unsigned char *)message->getNonce().c_str(),
			(const unsigned char *)key.c_str()) == 0) 
		? std::string((const char*)decrypted, decryptLength) : std::string("error");


	return decrypt(message, key);
}

CryptoBox CryptoHelper::encryptAndEncodeBase64(std::string input, std::string key) {

	CryptoBox encrypted = encrypt(input, key);	
	std::shared_ptr<CryptoBox> encryptedAndEncoded(new CryptoBox(encrypted.getValue(), encrypted.getNonce()));
	base64_encode(encryptedAndEncoded);

	encrypted.setMessage(encryptedAndEncoded->getValue());
	encrypted.setNonce(encryptedAndEncoded->getNonce());

	return encrypted;
}

std::string CryptoHelper::decodeBase64AndDecrypt(std::shared_ptr<CryptoBox> input, std::string key) {
	base64_decode(input);
	return decrypt(input, key);
}

KeyPairBox CryptoHelper::encryptAndEncodeBase64(std::shared_ptr<KeyPair> keyPair, std::string symKey) {
	CryptoBox box = encryptAndEncodeBase64(keyPair->getSecretKey(), symKey);
	std::string encodedPublicKey = base64_encode(keyPair->getPublicKey());
}
