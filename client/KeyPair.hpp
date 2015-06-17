#ifndef KEYPAIR_HPP
#define KEYPAIR_HPP

#include <string>

class KeyPair {

public:
	KeyPair(std::string privateKey, std::string publicKey);

	std::string getPrivateKey();
	std::string getPublicKey();	
	std::string getEncodedPrivateKey();
	std::string getEncodedPublicKey();

private:
	std::string m_privateKey;
	std::string m_publicKey;

};

#endif