#include "../include/user.hpp"
#include "../include/cryptohelper.hpp"

User::User(std::string username, std::shared_ptr<CryptoHelper> cryptoHelper)
		: m_username(username), m_cryptoHelper(cryptoHelper), m_userKeyPair(m_cryptoHelper->generateKeyPair()),
			m_exchangeKeyPair(m_cryptoHelper->generateKeyPair()) {

}

