#ifndef LRVIEWMODEL
#define LRVIEWMODEL
#include <QObject>
#include <QString>
#include <vector>
class LRViewModel:public QObject{
	Q_OBJECT
	Q_PROPERTY(QString name MEMBER mName NOTIFY nameChanged)
	Q_PROPERTY(QString user MEMBER mUser NOTIFY userChanged)
public:
	explicit LRViewModel(QObject* parent=nullptr):QObject(parent){}
signals:
	void nameChanged();
	void userChanged();
public slots:
	void testFunc();
private:
	QString mName="test";
	QString mUser="test";
};
#endif