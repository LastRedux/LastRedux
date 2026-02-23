import QtQuick
import QtQuick.Layouts
Item{
	property alias content:xLabel.content
	property alias href:xLink.href
	width:row.width
	height:20
	opacity:xLink.pressed?0.5:1
	Rectangle{
		anchors.fill:parent
		color:'#fff'
		opacity:xLink.hovered?0.375:0.25
		radius:999
	}
	RowLayout{
		id:row
		height:parent.height
		spacing:5
		LRLabel{
			id:xLabel
			size:'h3'
			style:Text.Normal
			Layout.leftMargin:8
			Layout.alignment:Qt.AlignVCenter
		}
		Image{
			Layout.rightMargin:3
			width:height
			height:parent.height-6
			source:'qrc:/ic_link.png'
		}
	}
	LRLink{
		id:xLink
		content:xLabel.content
	}
}