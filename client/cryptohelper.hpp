#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <iostream>
#include <sodium.h>
#include "keypair.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();

};

#endif