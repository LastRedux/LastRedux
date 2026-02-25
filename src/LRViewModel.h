#ifndef LRVIEWMODEL
#define LRVIEWMODEL
#include <QObject>
#include <QString>
#include <qtmetamacros.h>
#include "net/LRAPIWrapper.h"
class LRViewModel:public QObject{
	Q_OBJECT
	Q_PROPERTY(QString name MEMBER mName NOTIFY nameChanged)
	Q_PROPERTY(QString artist MEMBER mArtist NOTIFY artistChanged)
	Q_PROPERTY(QString album MEMBER mAlbum NOTIFY albumChanged)
	Q_PROPERTY(QString albumArt MEMBER mAlbumArt NOTIFY albumArtChanged)
public:
	explicit LRViewModel(QObject* parent=nullptr);
signals:
	void nameChanged();
	void artistChanged();
	void albumChanged();
	void albumArtChanged();
public slots:
	void fetchTrack();
private:
	LRAPIWrapper mAPI;
	QString mName="test";
	QString mArtist="test";
	QString mAlbum="test";
	QString mAlbumArt="";
};
#endif
