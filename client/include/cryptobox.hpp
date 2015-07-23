#ifndef CRYPTOBOX_HPP
#define CRYPTOBOX_HPP

#include <string>

class CryptoBox {

public:
	CryptoBox() {}
	CryptoBox(std::string value, std::string nonce) : m_value(value), m_nonce(nonce) {}
	std::string getValue() {return m_value;}
	std::string getNonce() {return m_nonce;}
	void setMessage(std::string value) {m_value = value;}
	void setNonce(std::string nonce) {m_nonce = nonce;}

protected:
	std::string m_value;
	std::string m_nonce;

};

#endif
