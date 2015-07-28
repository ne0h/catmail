#include "../include/newuserdialog.hpp"
#include "ui_newuserdialog.h"

NewUserDialog::NewUserDialog(std::shared_ptr<CryptoHelper> cryptoHelper, std::shared_ptr<Client> client,
							 QWidget *parent) :	QDialog(parent), ui(new Ui::NewUserDialog),
								m_cryptoHelper(cryptoHelper), m_client(client) {

	ui->setupUi(this);
}

NewUserDialog::~NewUserDialog() {
	delete ui;
}

void NewUserDialog::on_createUserBtn_released() {

	// password minimum length
	if (ui->passwordInpt->text().toStdString().size() < 8 && ui->usernameInpt->text().toStdString().size() > 1) {
		QMessageBox::information(NULL, "CatMail", "Minimum password length is 8 and username minimum length is 2.");
		return;
	}

	// compare passwords
	if (ui->passwordInpt->text().toStdString().compare(ui->passwordRepeatInpt->text().toStdString()) != 0) {
		QMessageBox::information(NULL, "CatMail", "Passwords do not match.");
		return;
	}

	const std::string storageHash = m_cryptoHelper->hash(std::make_shared<std::string>(ui->passwordInpt->text().toStdString()));
	const std::string loginHash   = m_cryptoHelper->hash(std::make_shared<std::string>(storageHash));

	std::shared_ptr<KeyPair> userKeyPair     = std::make_shared<KeyPair>(m_cryptoHelper->generateKeyPair());
	std::shared_ptr<KeyPair> exchangeKeyPair = std::make_shared<KeyPair>(m_cryptoHelper->generateKeyPair());

	const KeyPairBox encryptedUserKeyPair     = m_cryptoHelper->encryptAndEncodeBase64(userKeyPair, storageHash);
	const KeyPairBox encryptedExchangeKeyPair = m_cryptoHelper->encryptAndEncodeBase64(userKeyPair, storageHash);

	m_client->createUser(ui->usernameInpt->text().toStdString() + "@catmail.de", ui->passwordInpt->text().toStdString(),
						 std::make_shared<KeyPairBox>(encryptedUserKeyPair),
						 std::make_shared<KeyPairBox>(encryptedExchangeKeyPair));

	this->close();
}

void NewUserDialog::on_cancelBtn_released() {
	this->close();
}
