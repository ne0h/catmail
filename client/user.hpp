#ifndef USER_HPP
#define USER_HPP

#include <string>
#include "keypair.hpp"

class CryptoHelper;

class User {

public:
	User(std::string username, CryptoHelper *cryptoHelper);
	KeyPair* getUserKeyPair();
	KeyPair* getExchangeKeyPair();
	std::string getUsername();

private:
	CryptoHelper *m_cryptoHelper;
	const std::string m_username;
	KeyPair m_userKeyPair;
	KeyPair m_exchangeKeyPair;

};


#endif