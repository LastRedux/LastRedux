import QtQuick
import QtQuick.Layouts
Item{
	property alias value:label1.content
	property alias content:label2.content
	width:xColumn.width
	height:xColumn.height
	ColumnLayout{
		id:xColumn
		spacing:1
		LRLabel{id:label1;size:'num'}
		LRLabel{id:label2;size:'h4'}
	}
	LRLink{
		content:value
	}
}