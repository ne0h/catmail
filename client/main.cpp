#include <iostream>
#include <string>
#include <sodium.h>

#include "cryptohelper.hpp"
#include "keypair.hpp"
#include "user.hpp"
#include "contact.hpp"

using namespace std;

int main(int argc, char* argv[]) {

	CryptoHelper *cryptoHelper;
	User me("me", cryptoHelper);

	return 0;
}
