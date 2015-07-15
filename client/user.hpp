#ifndef USER_HPP
#define USER_HPP

#include <string>

#include "cryptohelper.hpp"

class User {

public:
	User(std::string username, CryptoHelper *cryptoHelper);

private:
	CryptoHelper *m_cryptoHelper;
	const std::string m_username;
	KeyPair m_userKeyPair;
	KeyPair m_exchangeKeyPair;

};


#endif