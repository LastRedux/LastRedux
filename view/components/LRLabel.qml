import QtQuick
import QtQuick.Controls
Label{
	id:root
	//h1,h2,h3,h4,num
	property string size:''
	property int weight:-1
	property alias content:root.text
	property alias align:root.horizontalAlignment
	property real alpha:size==="h4"?0.81:1
	property real alphaMod:1
	opacity:alphaMod===1?alpha:alpha*alphaMod
	renderType:Qt.platform.os==='osx'?Text.NativeRendering:Text.QtRendering
	style:Qt.platform.os==='osx'?Text.Sunken:Text.Normal
	styleColor:Qt.rgba(0,0,0,0.19)
	font{
		family:xFonts.name
		letterSpacing:{
			switch(size){
				case'h1':return -0.84
				case'h2':return -0.78
				case'h3':return 0
				case'h4':return 0.11
				case'num':return -0.6
				default:return -0.097
			}
		}
		pixelSize:{
			switch(size){
				case'h1':return 28
				case'h2':return 26
				case'h3':return 13
				case'h4':return 11
				case'num':return 20
				default:return 13
			}
		}
		weight:{
			if(weight!==-1)return weight
			switch(size){
				//case'num':return Font.ExtraBold
				case'':return Font.Normal
				default:return Font.Bold
			}
		}
	}
}