#!/bin/bash
BIN="$1"
QDEPLOY="$2"
VIEWDIR="$3"

if [ ! -d "${BIN}/LastRedux.app/Contents/Frameworks/QtQuick.framework" ]; then
	echo 'Deploying'
	"${QDEPLOY}" "${BIN}/LastRedux.app" -appstore-compliant -always-overwrite -qmldir="${VIEWDIR}"
else
	echo 'Deployed'
fi
