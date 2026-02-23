import QtQuick
import QtQuick.Layouts
RowLayout{
	property string content:""
	property int cw:-1
	property real value:0
	id:root
	spacing:8
	//PROGRESS
	Item{
		id:progress
		Layout.alignment:Qt.AlignVCenter
		Layout.minimumWidth:43
		Layout.fillWidth:true
		height:5
		LRTexture{res:'progress';xr:4;xl:4}
		Item{
			width:Math.max(0,Math.min(1,value))*parent.width
			height:parent.height
			LRTexture{res:content==='AS'?'progress_fm':'progress_active';xr:4;xl:4}
		}
	}
	//LABEL
	LRLabel{
		Layout.alignment:Qt.AlignVCenter
		Layout.minimumWidth:cw===-1?null:cw
		align:cw===-1?undefined:Text.AlignRight
		visible:content&&content!=='AS'
		alpha:0.81
		size:"h4"
		content:root.content
	}
	LRIcon{
		Layout.rightMargin:4
		size:9
		res:'as'
		visible:content==='AS'
	}
}