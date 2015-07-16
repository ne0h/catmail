#include "message.hpp"

Message::Message(std::string sender, std::string recipient, std::string message, std::string nonce)
		: m_sender(sender), m_recipient(recipient), m_message(message), m_nonce(nonce) {

}

std::string Message::getMessage() {
	return m_message;
}

std::string Message::getNonce() {
	return m_nonce;
}