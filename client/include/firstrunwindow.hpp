#ifndef FIRSTRUNWINDOW_HPP
#define FIRSTRUNWINDOW_HPP

#include <QMainWindow>

#include "newuserdialog.hpp"

#include "client.hpp"

namespace Ui {
class FirstRunWindow;
}

class FirstRunWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit FirstRunWindow(std::shared_ptr<CryptoHelper> cryptoHelper, std::shared_ptr<Client> client,
			    QWidget *parent = 0);
    ~FirstRunWindow();

private slots:
	void on_newUserBtn_released();

private:
    Ui::FirstRunWindow *ui;
    std::shared_ptr<CryptoHelper> m_cryptoHelper;
    std::shared_ptr<Client> m_client;
};

#endif // FIRSTRUNWINDOW_HPP
