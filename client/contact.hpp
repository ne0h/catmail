#ifndef CONTACT_HPP
#define CONTACT_HPP

#include <string>

class Contact {

public:
	Contact(const std::string username, const std::string userPublicKey, const std::string exchangePublicKey);

private:
	const std::string m_username;
	const std::string m_userPublicKey;
	const std::string m_exchangePublicKey;

};

#endif