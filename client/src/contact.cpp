#include "../include/contact.hpp"

Contact::Contact(const std::string username, const std::string userPublicKey, const std::string exchangePublicKey)
		: m_username(username), m_userPublicKey(userPublicKey), m_exchangePublicKey(exchangePublicKey) {

}

std::string Contact::getUsername() {
	return m_username;
}

std::string Contact::getUserPublicKey() {
	return m_userPublicKey;
}