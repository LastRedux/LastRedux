#include "LRViewModel.h"
void LRViewModel::testFunc(){
	mName="ChangedName";
	mUser="ChangedUser";
	emit nameChanged();
	emit userChanged();
}