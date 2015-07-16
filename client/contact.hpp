#ifndef CONTACT_HPP
#define CONTACT_HPP

#include <string>

class Contact {

public:
	Contact(const std::string username, const std::string userPublicKey, const std::string exchangePublicKey);
	std::string getUsername();
	std::string getUserPublicKey();

private:
	std::string m_username;
	std::string m_userPublicKey;
	std::string m_exchangePublicKey;

};

#endif