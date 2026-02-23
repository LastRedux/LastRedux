import QtQuick
Item{
	property string base:'song_m'
	width:34
	height:34
	LRTexture{res:'cover'}
	LRIcon{anchors.centerIn:parent;res:base}
}