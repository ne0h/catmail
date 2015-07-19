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

void CryptoBox::setMessage(std::string message) {
	m_message = message;
}

void CryptoBox::setNonce(std::string nonce) {
	m_nonce = nonce;
}
