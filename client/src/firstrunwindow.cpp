#include "../include/firstrunwindow.hpp"
#include "../include/newuserdialog.hpp"
#include "ui_firstrunwindow.h"

FirstRunWindow::FirstRunWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::FirstRunWindow) {
    ui->setupUi(this);

}

FirstRunWindow::~FirstRunWindow() {
    delete ui;
}

void FirstRunWindow::on_newUserBtn_released() {
	NewUserDialog *newUserDialog = new NewUserDialog();
	newUserDialog->show();
}
