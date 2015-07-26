#include "../include/firstrunwindow.hpp"
#include "ui_firstrunwindow.h"

FirstRunWindow::FirstRunWindow(std::shared_ptr<Client> client, QWidget *parent) : QMainWindow(parent),
		ui(new Ui::FirstRunWindow), m_client(client) {

	ui->setupUi(this);
}

FirstRunWindow::~FirstRunWindow() {
    delete ui;
}

void FirstRunWindow::on_newUserBtn_released() {
	NewUserDialog *newUserDialog = new NewUserDialog(m_client);
	newUserDialog->show();
}
