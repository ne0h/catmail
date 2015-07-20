#ifndef CRYPTOBOX_HPP
#define CRYPTOBOX_HPP

#include <string>

class CryptoBox {

public:
	CryptoBox();
	CryptoBox(std::string message, std::string nonce);
	std::string getMessage();
	std::string getNonce();
	void setMessage(std::string message);
	void setNonce(std::string nonce);

protected:
	std::string m_message;
	std::string m_nonce;

};

#endif
