#include <iostream>

#include "cryptohelper.hpp"
#include "KeyPair.hpp"

using namespace std;

int main() {

	CryptoHelper *cryptoHelper;
	KeyPair keyPair = cryptoHelper->generateKeyPair();

	return 0;
}
