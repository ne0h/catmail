#ifndef CRYPTOHELPER_HPP
#define CRYPTOHELPER_HPP

#include <iostream>
#include <sodium.h>
#include "KeyPair.hpp"

class CryptoHelper {

public:
	CryptoHelper();
	KeyPair generateKeyPair();

};

#endif
