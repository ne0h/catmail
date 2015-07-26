#include "../include/newuserdialog.hpp"
#include "ui_newuserdialog.h"

NewUserDialog::NewUserDialog(std::shared_ptr<Client> client, QWidget *parent) :	QDialog(parent),
		ui(new Ui::NewUserDialog), m_client(client) {

	ui->setupUi(this);
}

NewUserDialog::~NewUserDialog() {
	delete ui;
}

void NewUserDialog::on_createUserBtn_released() {

	// password minimum length
	if (ui->passwordInpt->text().toStdString().size() < 8) {
		QMessageBox::information(NULL, "CatMail", "Minimum password length is 8.");
	}

	// compare passwords
	if (ui->passwordInpt->text().toStdString().compare(ui->passwordRepeatInpt->text().toStdString()) != 0) {
		QMessageBox::information(NULL, "CatMail", "Passwords do not match.");
		return;
	}

	CryptoHelper cryptoHelper;

	std::shared_ptr<KeyPair> userKeyPair     = std::make_shared<KeyPair>(cryptoHelper.generateKeyPair());
	std::shared_ptr<KeyPair> exchangeKeyPair = std::make_shared<KeyPair>(cryptoHelper.generateKeyPair());

	const std::string symKey = ui->passwordInpt->text().toStdString();
	const KeyPairBox encryptedUserKeyPair     = cryptoHelper.encryptAndEncodeBase64(userKeyPair, symKey);
	const KeyPairBox encryptedExchangeKeyPair = cryptoHelper.encryptAndEncodeBase64(userKeyPair, symKey);
}

void NewUserDialog::on_cancelBtn_released() {
	this->close();
}
