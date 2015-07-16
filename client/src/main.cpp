#include <iostream>
#include <string>
#include <sodium.h>

#include "../include/cryptohelper.hpp"
#include "../include/keypair.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"

#include <QApplication>
#include "../include/mainwindow.hpp"

using namespace std;

int main(int argc, char* argv[]) {

	QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
