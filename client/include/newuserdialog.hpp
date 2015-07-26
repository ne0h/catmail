#ifndef NEWUSERDIALOG_HPP
#define NEWUSERDIALOG_HPP

#include <QDialog>
#include <QMessageBox>

#include "client.hpp"
#include "cryptohelper.hpp"

namespace Ui {
class NewUserDialog;
}

class NewUserDialog : public QDialog
{
	Q_OBJECT

public:
    explicit NewUserDialog(std::shared_ptr<Client> client, QWidget *parent = 0);
    ~NewUserDialog();

private slots:
    void on_createUserBtn_released();
    void on_cancelBtn_released();

private:
	Ui::NewUserDialog *ui;
	std::shared_ptr<Client> m_client;
};

#endif // NEWUSERDIALOG_HPP
