#include "keypair.hpp"

KeyPair::KeyPair(std::string secretKey, std::string publicKey)
		: m_secretKey(secretKey), m_publicKey(publicKey) {
}

std::string KeyPair::getSecretKey() {
	return m_secretKey;
}

std::string KeyPair::getPublicKey() {
	return m_publicKey;
}
