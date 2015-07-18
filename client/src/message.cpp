#include "../include/message.hpp"

Message::Message(std::string sender, std::string recipient, std::string message, std::string nonce)
		: m_sender(sender), m_recipient(recipient), CryptoBox(message, nonce) {

}
