#include <iostream>
#include <string>
#include <sodium.h>

#include "../include/cryptohelper.hpp"
#include "../include/keypair.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"

using namespace std;

int main(int argc, char* argv[]) {

	CryptoHelper *cryptoHelper;
	User me("me", cryptoHelper);

	return 0;
}
