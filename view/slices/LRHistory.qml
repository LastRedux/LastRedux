import QtQuick
import QtQuick.Layouts
Item{
	Flickable{
		anchors.fill:parent
		id:xFlick
		contentHeight:xColumn.height
		clip:true
		ColumnLayout{
			id:xColumn
			width:parent.width
			spacing:0
			LRHead{
				content:'NOW SCROBBLING'
				child:Component{
					LRProgress{
						content:'AS'
						value:0.25
					}
				}
			}
			LREntry{
				active:true
				content:'song'
				sub:'artist'
			}
			LRHead{
				content:'HISTORY'
			}
			Repeater{
				model:25
				LREntry{
					content:'song'
					sub:'artist'
					date:'2/18/2026 6:22pm'
				}
			}
		}
	}
	LRScroll{
		anchors.fill:xFlick
		hook:xFlick
	}
}