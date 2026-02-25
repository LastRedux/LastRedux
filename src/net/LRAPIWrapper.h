#ifndef LRAPIWRAPPER
#define LRAPIWRAPPER

#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QObject>
#include <QString>
#include <QUrl>
#include <QVector>

struct LRArtist {
	QString url;
	QString name;
};

struct LRTag {
	QString name;
	QString url;
};

struct LRTrack {
	QString url;
	QString name;
	QString image;
	QString album;
	LRArtist artist;
	int plays = 0;
	bool loved = false;
	int allListeners = 0;
	int allPlays = 0;
	QVector<LRTag> tags;
};

class LRAPIWrapper : public QObject {
	Q_OBJECT
  public:
	explicit LRAPIWrapper(QObject* parent = nullptr);
	void setUsername(const QString& username);
	void getTrack(const QString& artist, const QString& name);
  signals:
	void trackGot(const LRTrack& track);
	void trackError(const QString& errorMessage);

  private:
	static constexpr const char* KEY = "c9205aee76c576c84dc372de469dcb00";
	static constexpr const char* BASE = "https://ws.audioscrobbler.com/2.0/";
	static constexpr const char* UA = "LastRedux/1.0";
	QNetworkAccessManager mNet;
	QString mUsername;
	QNetworkReply* req(QMap<QString, QString> params);
	LRTrack parseTrack(const QJsonObject& trackObj) const;
};
#endif
