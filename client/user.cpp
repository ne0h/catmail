#include "user.hpp"

User::User(std::string username, CryptoHelper *cryptoHelper)
		: m_username(username), m_cryptoHelper(cryptoHelper), m_userKeyPair(m_cryptoHelper->generateKeyPair()),
			m_exchangeKeyPair(m_cryptoHelper->generateKeyPair()) {

}