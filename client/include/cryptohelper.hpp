#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <memory>

#include <sodium.h>

#include "keypair.hpp"
#include "user.hpp"
#include "message.hpp"
#include "contact.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();
	Message encryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message);
	std::string decryptAsym(std::shared_ptr<User> user, std::shared_ptr<Contact> sender,
		std::shared_ptr<Message> message);

	std::string generateSecretKey();
	Message encrypt(std::shared_ptr<User> user, std::shared_ptr<Contact> recipient, std::string message,
		std::string key);
	std::string decrypt(std::shared_ptr<User> user, std::shared_ptr<Message> message, std::string key);

};

#endif
