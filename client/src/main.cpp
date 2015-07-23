#include <iostream>
#include <string>
#include <sodium.h>

#include "../include/cryptohelper.hpp"
#include "../include/keypair.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"
#include "../include/client.hpp"

#include <QApplication>
#include "../include/firstrunwindow.hpp"
#include "../include/mainwindow.hpp"

using namespace std;

int main(int argc, char* argv[]) {

	std::unique_ptr<Client> client(new Client("miauuu.de", 5000));
	std::shared_ptr<KeyPair> userKeyPair(new KeyPair("secretKey", "publicKey"));
	std::shared_ptr<KeyPair> exchangeKeyPair(new KeyPair("11secretKey", "11publicKey"));

	client->createUser("cat", "cat_key", userKeyPair, exchangeKeyPair);

	return 0;

	/*QApplication a(argc, argv);
    FirstRunWindow w;
    w.show();

	return a.exec();*/
}
