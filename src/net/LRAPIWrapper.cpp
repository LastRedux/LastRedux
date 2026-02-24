#include "LRAPIWrapper.h"
#include <QUrlQuery>

LRAPIWrapper::LRAPIWrapper(QObject* parent):QObject(parent){}

void LRAPIWrapper::setUsername(const QString& username){
    mUsername = username;
}

QNetworkReply* LRAPIWrapper::req(QMap<QString, QString> params){
    params["api_key"] = KEY;
    params["format"] = "json";
    if (!mUsername.isEmpty() && !params.contains("username")) {
        params["username"] = mUsername;
    }

    QUrl url(BASE);
    QUrlQuery query;
    for (auto it = params.constBegin(); it != params.constEnd(); ++it) {
        query.addQueryItem(it.key(), it.value());
    }
    url.setQuery(query);

    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::UserAgentHeader, UA);

    return mNet.get(request);
}

void LRAPIWrapper::getTrack(const QString& artist, const QString& name)
{
    QNetworkReply* reply = req({
        {"method", "track.getInfo"},
        {"artist", artist},
        {"track", name}
    });

    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        reply->deleteLater();

        if (reply->error() != QNetworkReply::NoError) {
            emit trackError(reply->errorString());
            return;
        }

        QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
        if (doc.isNull() || !doc.isObject()) {
            emit trackError("Invalid JSON response");
            return;
        }

        QJsonObject root = doc.object();
        if (root.contains("error")) {
            emit trackError(root["message"].toString());
            return;
        }

        if (!root.contains("track")) {
            emit trackError("Missing track data in response");
            return;
        }

        emit trackGot(parseTrack(root["track"].toObject()));
    });
}

LRTrack LRAPIWrapper::parseTrack(const QJsonObject& trackObj) const
{
    LRTrack info;

    info.url = trackObj["url"].toString();
    info.name = trackObj["name"].toString();

    QJsonObject artistObj = trackObj["artist"].toObject();
    info.artist.name = artistObj["name"].toString();
    info.artist.url = artistObj["url"].toString();

    info.plays = trackObj["userplaycount"].toString().toInt();
    info.loved = trackObj["userloved"].toString() == "1";
    info.allListeners = trackObj["listeners"].toString().toInt();
    info.allPlays = trackObj["playcount"].toString().toInt();

    QJsonObject toptagsObj = trackObj["toptags"].toObject();
    QJsonArray tagsArray = toptagsObj["tag"].toArray();
    for (const QJsonValue& tagVal : tagsArray) {
        QJsonObject tagObj = tagVal.toObject();
        LRTag tag;
        tag.name = tagObj["name"].toString();
        tag.url = tagObj["url"].toString();
        info.tags.append(tag);
    }

    return info;
}
