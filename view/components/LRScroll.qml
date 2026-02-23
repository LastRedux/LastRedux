import QtQuick
MouseArea{
	property Flickable hook
	property real minX:hook.originX-hook.leftMargin
	property real maxX:hook.contentWidth+hook.rightMargin+hook.originX-hook.width
	property real minY:hook.originY-hook.topMargin
	property real maxY:hook.contentHeight+hook.bottomMargin+hook.originY-hook.height
	propagateComposedEvents:true
	z:-1
	onHookChanged:{
		hook.boundsBehavior=Flickable.StopAtBounds
		hook.pixelAligned=true
		hook.interactive=false
	}
	function angleToPx(delta){
		return ((delta/8)/15.0)*20*Qt.styleHints.wheelScrollLines
	}
	function scrollX(dx){
		if(!dx)return hook.contentX
		return Math.max(minX,Math.min(maxX,hook.contentX-dx))
	}
	function scrollY(dy){
		if(!dy)return hook.contentY
		return Math.max(minY,Math.min(maxY,hook.contentY-dy))
	}
	function getNewX(wheel){
		if(
			(hook.contentWidth<hook.width)||
			(wheel.pixelDelta.x===0)
		){
			return hook.contentX
		}
		return scrollX(wheel.pixelDelta.x)
	}
	function getNewY(wheel){
		if(
			(hook.contentHeight<hook.height)||
			(wheel.pixelDelta.y&&wheel.angleDelta===0)
		){
			return hook.contentY
		}
		if(wheel.angleDelta.y){
			return scrollY(angleToPx(wheel.angleDelta.y))
		}
		return scrollY(wheel.pixelDelta.y)
	}
	onWheel:function(wheel){
		if(hook.scrolling!==undefined)hook.scrolling=true
		hook.contentX=getNewX(wheel)
		hook.contentY=getNewY(wheel)
	}
}