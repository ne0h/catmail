#ifndef KEYPAIR_HPP
#define KEYPAIR_HPP

#include <string>

class KeyPair {

public:
	KeyPair(std::string secretKey, std::string publicKey) : m_secretKey(secretKey), m_publicKey(publicKey) {}

	std::string getSecretKey() {return m_secretKey;}
	std::string getPublicKey() {return m_publicKey;}

private:
	std::string m_secretKey;
	std::string m_publicKey;

};

#endif
