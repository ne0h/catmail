#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <sodium.h>

#include "keypair.hpp"
#include "user.hpp"
#include "message.hpp"
#include "contact.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();
	Message encryptAsym(User *user, Contact *recipient, std::string message);
	std::string decryptAsym(User *user, Contact *sender, Message *message);

	std::string generateSecretKey();
	Message encrypt(User *user, Contact *recipient, std::string message, std::string key);
	std::string decrypt(User *user, Message *message, std::string key);

};

#endif
