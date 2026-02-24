#ifndef LRVIEWMODEL
#define LRVIEWMODEL
#include <QObject>
#include <QString>
#include <vector>
class LRViewModel:public QObject{
	Q_OBJECT
	Q_PROPERTY(QString name MEMBER mName NOTIFY nameChanged)
	Q_PROPERTY(QString artist MEMBER mArtist NOTIFY artistChanged)
	Q_PROPERTY(QString album MEMBER mAlbum NOTIFY albumChanged)
public:
	explicit LRViewModel(QObject* parent=nullptr):QObject(parent){}
signals:
	void nameChanged();
	void artistChanged();
	void albumChanged();
public slots:
	void fetchTrack();
private:
	LRAPIWrapper mAPI;
	QString mName="test";
	QString mArtist="test";
	QString mAlbum="test";
};
#endif
