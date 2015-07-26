#ifndef KEYPAIRBOX_H
#define KEYPAIRBOX_H

#include <string>

#include "cryptobox.hpp"

class KeyPairBox : public CryptoBox {

public:
	KeyPairBox(std::string secretKey, std::string nonce, std::string publicKey) : CryptoBox(secretKey, nonce),
		m_publicKey(publicKey) {}
	std::string getPublicKey() {return m_publicKey;}

private:
	std::string m_publicKey;

};

#endif // KEYPAIRBOX_H
