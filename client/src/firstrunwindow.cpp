#include "../include/firstrunwindow.hpp"
#include "ui_firstrunwindow.h"

FirstRunWindow::FirstRunWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::FirstRunWindow)
{
    ui->setupUi(this);
}

FirstRunWindow::~FirstRunWindow()
{
    delete ui;
}
