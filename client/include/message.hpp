#ifndef MESSAGE_HPP
#define MESSAGE_HPP

#include <string>

#include "cryptobox.hpp"

class Message : public CryptoBox {

public:
	Message(std::string sender, std::string recipient, std::string message, std::string nonce) :
	    CryptoBox(message, nonce), m_sender(sender), m_recipient(recipient) {}
	const std::string getSender();
	const std::string getRecipient();

private:
	const std::string m_sender;
	const std::string m_recipient;

};

#endif
