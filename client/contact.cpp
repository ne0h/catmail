#include "contact.hpp"

Contact::Contact(const std::string username, const std::string userPublicKey, const std::string exchangePublicKey)
		: m_username(username), m_userPublicKey(userPublicKey), m_exchangePublicKey(exchangePublicKey) {

}