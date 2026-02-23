import QtQuick
import QtQuick.Layouts
Item{
	property bool pause:true
	property bool big:false
	id:root
	width:big?31:18
	height:big?31:18
	LRTexture{
		res:big?'playing_lg':'playing'
	}
	RowLayout{
		anchors.centerIn:parent
		height:big?17:10
		spacing:big?4:2
		Repeater{
			model:3
			Item{
				required property int index
				property int ms:175*(index+1)
				Layout.fillHeight:true
				width:big?3:2
				Rectangle{
					id:bar
					y:parent.height-height
					width:parent.width
					radius:999
				}
				states:State{
					name:'paused'
					when:!root.visible||root.pause
					PropertyChanges{target:anim;running:false}
				}
				transitions:Transition{
					from:''
					to:'paused'
					NumberAnimation{
						target:bar
						property:'height'
						to:width
						duration:bar.height*10
					}
				}
				SequentialAnimation{
					id:anim
					loops:Animation.Infinite
					running:true
					NumberAnimation{
						target:bar
						property:'height'
						from:0
						to:height
						duration:ms
					}
					NumberAnimation{
						target:bar
						property:'height'
						from:height
						to:0
						duration:ms
					}
				}
			}
		}
	}
}