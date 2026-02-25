import QtQuick
Item{
	property string base:'song_m'
	property string image:''
	property int iconSize:20
	width:34
	height:34
	LRTexture{res:'cover'}
	LRIcon{
		anchors.centerIn:parent
		res:base
		size:iconSize
		visible:image===''
	}
	Image{
		anchors.fill:parent
		source:image
		visible:image!==''
	}
}
