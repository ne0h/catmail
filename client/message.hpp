#ifndef MESSAGE_HPP
#define MESSAGE_HPP

#include <string>

class Message {

public:
	Message(std::string sender, std::string recipient, std::string message, std::string nonce);
	const std::string getSender();
	const std::string getRecipient();
	std::string getMessage();
	std::string getNonce();

private:
	const std::string m_sender;
	const std::string m_recipient;
	std::string m_message;
	std::string m_nonce;

};

#endif