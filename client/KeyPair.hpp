#ifndef KEYPAIR_HPP
#define KEYPAIR_HPP

#include <string>

class KeyPair {

public:
	KeyPair(std::string privateKey, std::string publicKey);

private:
	std::string privateKey;
	std::string publicKey;

};

#endif