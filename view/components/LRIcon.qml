import QtQuick
Item{
	property int size:20
	property string res:''
	width:size
	height:size
	Image{
		anchors.horizontalCenter:parent.horizontalCenter
		fillMode:Image.PreserveAspectCrop
		source:'qrc:/ic_'+res+'.png'
		height:size+20
		y:-10
	}
}