#ifndef FIRSTRUNWINDOW_HPP
#define FIRSTRUNWINDOW_HPP

#include <QMainWindow>

namespace Ui {
class FirstRunWindow;
}

class FirstRunWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit FirstRunWindow(QWidget *parent = 0);
    ~FirstRunWindow();

private slots:
	void on_newUserBtn_released();

private:
    Ui::FirstRunWindow *ui;
};

#endif // FIRSTRUNWINDOW_HPP