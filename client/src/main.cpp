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

	std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper);
	std::shared_ptr<Client> client(new Client("miauuu.de", 5000));

	QApplication a(argc, argv);
	FirstRunWindow w(cryptoHelper, client);
    w.show();

	return a.exec();
}
