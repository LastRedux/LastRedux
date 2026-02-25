#include "LRAPIWrapper.h"
#include <QUrlQuery>

LRAPIWrapper::LRAPIWrapper(QObject* parent) : QObject(parent) {}

void LRAPIWrapper::setUsername(const QString& username) {
	mUsername = username;
}

QNetworkReply* LRAPIWrapper::req(QMap<QString, QString> params) {
	params["api_key"] = KEY;
	params["format"] = "json";
	if(!mUsername.isEmpty() && !params.contains("username")) {
		params["username"] = mUsername;
	}

	QUrl url(BASE);
	QUrlQuery query;
	for(auto it = params.constBegin(); it != params.constEnd(); ++it) {
		query.addQueryItem(it.key(), it.value());
	}
	url.setQuery(query);

	QNetworkRequest request(url);
	request.setHeader(QNetworkRequest::UserAgentHeader, UA);

	return mNet.get(request);
}

void LRAPIWrapper::getTrack(const QString& artist, const QString& name) {
	QNetworkReply* reply = req({{"method", "track.getInfo"},
		{"artist", artist},
		{"track", name}});

	connect(reply, &QNetworkReply::finished, this, [this, reply]() {
		reply->deleteLater();

		if(reply->error() != QNetworkReply::NoError) {
			emit trackError(reply->errorString());
			return;
		}

		QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
		if(doc.isNull() || !doc.isObject()) {
			emit trackError("Invalid JSON response");
			return;
		}

		QJsonObject root = doc.object();
		if(root.contains("error")) {
			emit trackError(root["message"].toString());
			return;
		}

		if(!root.contains("track")) {
			emit trackError("Missing track data in response");
			return;
		}

		LRTrack info = parseTrack(root["track"].toObject());

		if(!info.image.isEmpty()) {
			// we have to try to get the image data ourselves
			// because last.fm's CDN is sometimes not happy
			// with QML's built-in network requests
			QNetworkRequest req((QUrl(info.image)));
			req.setHeader(QNetworkRequest::UserAgentHeader, UA);
			QNetworkReply* rply = mNet.get(req);

			connect(rply, &QNetworkReply::finished, this, [this, info, rply]() mutable {
				rply->deleteLater();
				if(rply->error() == QNetworkReply::NoError) {
					QByteArray img = rply->readAll();
					info.image = "data:image/png;base64," + img.toBase64();
				} else {
				}
				emit trackGot(info);
			});
		} else {
			emit trackGot(info);
		}
	});
}

LRTrack LRAPIWrapper::parseTrack(const QJsonObject& trackObj) const {
	LRTrack info;

	info.url = trackObj["url"].toString();
	info.name = trackObj["name"].toString();

	QJsonObject artistObj = trackObj["artist"].toObject();
	info.artist.name = artistObj["name"].toString();
	info.artist.url = artistObj["url"].toString();

	QJsonObject albumObj = trackObj["album"].toObject();
	info.album = albumObj["title"].toString();

	QJsonArray images = albumObj["image"].toArray();
	if(!images.isEmpty()) {
		QStringList sizePriority = {"mega", "extralarge",
			"large", "medium", "small"};

		for(const QString& size : sizePriority) {
			bool found = false;
			for(const QJsonValue& img : images) {
				QJsonObject imgObj = img.toObject();
				if(imgObj["size"].toString() == size &&
					!imgObj["#text"].toString().isEmpty()) {
					info.image = imgObj["#text"].toString();
					found = true;
					break;
				}
			}
			if(found) break;
		}
	}

	info.plays = trackObj["userplaycount"].toString().toInt();
	info.loved = trackObj["userloved"].toString() == "1";
	info.allListeners = trackObj["listeners"].toString().toInt();
	info.allPlays = trackObj["playcount"].toString().toInt();

	QJsonObject toptagsObj = trackObj["toptags"].toObject();
	QJsonArray tagsArray = toptagsObj["tag"].toArray();
	for(const QJsonValue& tagVal : tagsArray) {
		QJsonObject tagObj = tagVal.toObject();
		LRTag tag;
		tag.name = tagObj["name"].toString();
		tag.url = tagObj["url"].toString();
		info.tags.append(tag);
	}

	return info;
}
