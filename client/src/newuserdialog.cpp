#include "newuserdialog.hpp"
#include "ui_newuserdialog.h"

NewUserDialog::NewUserDialog(QWidget *parent) :
	QDialog(parent),
	ui(new Ui::NewUserDialog)
{
	ui->setupUi(this);
}

NewUserDialog::~NewUserDialog()
{
	delete ui;
}
