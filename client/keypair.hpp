#ifndef KEYPAIR_HPP
#define KEYPAIR_HPP

#include <string>

class KeyPair {

public:
	KeyPair(std::string secretKey, std::string publicKey);

	std::string getSecretKey();
	std::string getPublicKey();	
	std::string getEncodedPrivateKey();
	std::string getEncodedPublicKey();

private:
	std::string m_secretKey;
	std::string m_publicKey;

};

#endif
