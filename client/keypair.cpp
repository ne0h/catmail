#include "keypair.hpp"

KeyPair::KeyPair(std::string privateKey, std::string publicKey) {

	m_privateKey = privateKey;
	m_publicKey  = publicKey;
}

std::string KeyPair::getPrivateKey() {
	return m_privateKey;
}

std::string KeyPair::getPublicKey() {
	return m_publicKey;
}
