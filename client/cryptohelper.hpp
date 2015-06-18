#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <iostream>
#include <sodium.h>
#include "keypair.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();
	std::string encodeAsym(std::string message, std::string nonce, std::string recipientPublicKey,
		std::string senderPrivateKey);
	std::string decodeAsym(std::string cipherText, std::string nonce, std::string recipientPrivateKey,
		std::string senderPublicKey);

};

#endif
