#include <iostream>

#include "cryptohelper.hpp"
#include "keypair.hpp"

using namespace std;

int main() {

	CryptoHelper *cryptoHelper;
	KeyPair keyPair = cryptoHelper->generateKeyPair();

	return 0;
}
