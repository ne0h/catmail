#include "../include/newuserdialog.hpp"
#include "ui_newuserdialog.h"

NewUserDialog::NewUserDialog(QWidget *parent) :	QDialog(parent), ui(new Ui::NewUserDialog) {
	ui->setupUi(this);
}

NewUserDialog::~NewUserDialog() {
	delete ui;
}

void NewUserDialog::on_createUserBtn_released() {
	CryptoHelper cryptoHelper;

	std::shared_ptr<KeyPair> userKeyPair     = std::make_shared<KeyPair>(cryptoHelper.generateKeyPair());
	std::shared_ptr<KeyPair> exchangeKeyPair = std::make_shared<KeyPair>(cryptoHelper.generateKeyPair());

	KeyPairBox encryptedUserKeyPair = cryptoHelper.encryptAndEncodeBase64(userKeyPair, ui->passwordInpt->text().toStdString());
}

void NewUserDialog::on_cancelBtn_released() {
	this->close();
}
