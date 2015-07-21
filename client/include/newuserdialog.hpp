#ifndef NEWUSERDIALOG_HPP
#define NEWUSERDIALOG_HPP

#include <QDialog>

namespace Ui {
class NewUserDialog;
}

class NewUserDialog : public QDialog
{
	Q_OBJECT

public:
	explicit NewUserDialog(QWidget *parent = 0);
	~NewUserDialog();

private:
	Ui::NewUserDialog *ui;
};

#endif // NEWUSERDIALOG_HPP
