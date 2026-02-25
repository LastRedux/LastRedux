#include "LRViewModel.h"
LRViewModel::LRViewModel(QObject* parent):QObject(parent){
	connect(&mAPI, &LRAPIWrapper::trackGot, this, [this](const LRTrack& track){
			mName = track.name;
			mArtist = track.artist.name;
			mAlbum = track.album;
			mAlbumArt = track.image;
			mTags.clear();
			for(const LRTag& tag : track.tags){
				QVariantMap tagMap;
				tagMap["name"] = tag.name;
				tagMap["url"] = tag.url;
				mTags.append(tagMap);
			}
			emit nameChanged();
			emit artistChanged();
			emit albumChanged();
			emit albumArtChanged();
			emit tagsChanged();
			});
	connect(&mAPI, &LRAPIWrapper::trackError, [this](const QString& error){
			qWarning() << "failed to get track: " << error;
			});

}

void LRViewModel::fetchTrack(){
	mAPI.getTrack("Porter Robinson", "Cheerleader");
}
