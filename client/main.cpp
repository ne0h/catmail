#include <iostream>
#include <string>
#include <sodium.h>

#include "cryptohelper.hpp"
#include "keypair.hpp"
#include "user.hpp"
#include "contact.hpp"

using namespace std;

int main() {

	CryptoHelper *cryptoHelper;
	User ne0h("ne0h", cryptoHelper);

	/*string text = "dasistdergeheimetextxxx";
	CryptoHelper *cryptoHelper;
	KeyPair alice = cryptoHelper->generateKeyPair();

	unsigned char nonce[crypto_box_NONCEBYTES];
	randombytes_buf(nonce, sizeof nonce);
	unsigned char ciphertext[text.size()];

	crypto_box_easy(ciphertext, (const unsigned char *)text.c_str(), text.size(), nonce,
		(const unsigned char *)alice.getPublicKey().c_str(),
		(const unsigned char *)alice.getSecretKey().c_str());

	unsigned char decrypted[text.size()];
	crypto_box_open_easy(decrypted, ciphertext, crypto_box_MACBYTES + text.size(), nonce,
		(const unsigned char *)alice.getPublicKey().c_str(),
		(const unsigned char *)alice.getSecretKey().c_str());

	cout << decrypted << endl;*/

	return 0;
}
