import QtQuick
import QtQuick.Layouts
RowLayout{
	property string content:''
	property string suffix:''
	property alias res:xIcon.res
	id:xRoot
	Layout.fillWidth:parent
	spacing:10
	height:20
	LRIcon{id:xIcon}
	LRLabel{
		content:xRoot.content+' '+xRoot.suffix
		Layout.fillWidth:parent
		size:'h3'
		LRLink{content:xRoot.content}
	}
}