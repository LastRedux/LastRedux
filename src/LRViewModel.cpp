#include "LRViewModel.h"
void LRViewModel::fetchTrack(){
	mAPI.getTrack("Madeon", "No Fear No More");
	emit nameChanged();
	emit artistChanged();
	emit albumChanged();
}
