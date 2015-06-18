#include <iostream>

#include "cryptohelper.hpp"
#include "keypair.hpp"

using namespace std;

int main() {

	CryptoHelper *cryptoHelper;
	KeyPair alice = cryptoHelper->generateKeyPair();
	KeyPair bob   = cryptoHelper->generateKeyPair();

	std::string message = "secrettesttext";
	unsigned char nonce[crypto_box_NONCEBYTES];
	randombytes_buf(nonce, sizeof nonce);
	std::string n = string((char*) nonce);

	std::string cipherText = cryptoHelper->encodeAsym(message, n, bob.getPublicKey(), alice.getPrivateKey());
	std::string result     = cryptoHelper->decodeAsym(cipherText, n, bob.getPrivateKey(), alice.getPublicKey());

	cout << result << endl;

	return 0;
}
