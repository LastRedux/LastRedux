#include "LRViewModel.h"
LRViewModel::LRViewModel(QObject* parent):QObject(parent){
	connect(&mAPI, &LRAPIWrapper::trackGot, this, [this](const LRTrack& track){
			mName = track.name;
			mArtist = track.artist.name;
			mAlbum = track.album;
			mAlbumArt = track.image;
			emit nameChanged();
			emit artistChanged();
			emit albumChanged();
			emit albumArtChanged();
			});
	connect(&mAPI, &LRAPIWrapper::trackError, this, [this](const QString& error){
			qWarning() << "failed to get track: " << error;
			});

}

void LRViewModel::fetchTrack(){
	mAPI.getTrack("Porter Robinson", "Cheerleader");
}
