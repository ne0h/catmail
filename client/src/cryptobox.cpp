#include "cryptobox.hpp"

CryptoBox::CryptoBox(std::string message, std::string nonce)
		: m_message(message), m_nonce(nonce) {

}

std::string CryptoBox::getMessage() {
	return m_message;
}

std::string CryptoBox::getNonce() {
	return m_nonce;
}