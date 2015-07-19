#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <memory>

#include <sodium.h>

#include "keypair.hpp"
#include "user.hpp"
#include "message.hpp"
#include "contact.hpp"
#include "cryptobox.hpp"
#include "base64.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();
	Message encryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message);
	std::string decryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> sender,
		std::shared_ptr<Message> message);

	std::string generateSymKey();

	CryptoBox encrypt(std::string message, std::string key);
	Message encrypt(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message,
		std::string key);

	std::string decrypt(std::shared_ptr<CryptoBox> message, std::string key);
	std::string decrypt(std::shared_ptr<User> user, std::shared_ptr<Message> message, std::string key);

	CryptoBox encryptAndEncodeBase64(std::string input, std::string key);
	std::string decodeBase64AndDecrypt(std::shared_ptr<CryptoBox> input);

};

#endif
