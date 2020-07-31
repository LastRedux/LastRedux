import QtQuick 2.14

MouseArea {
	property Flickable flickable
	property real minimumXExtent: flickable.originX - flickable.leftMargin
	property real maximumXExtent: flickable.contentWidth + flickable.rightMargin + flickable.originX - flickable.width
	property real minimumYExtent: flickable.originY - flickable.topMargin
	property real maximumYExtent: flickable.contentHeight + flickable.bottomMargin + flickable.originY - flickable.height
	
	propagateComposedEvents: true
	z: -1
	
	onFlickableChanged: {
		flickable.boundsBehavior = Flickable.StopAtBounds
		flickable.interactive = false
		flickable.pixelAligned = true
	}
	
	function scrollXByPixelDelta(pixelDelta) {
		if (!pixelDelta) {
			return flickable.contentX
		}
		
		return Math.max(minimumXExtent, Math.min(maximumXExtent, flickable.contentX - pixelDelta))
	}
	
	function scrollYByPixelDelta(pixelDelta) {
		if (!pixelDelta) {
			return flickable.contentY
		}
		
		return Math.max(minimumYExtent, Math.min(maximumYExtent, flickable.contentY - pixelDelta))
	}
	
	function pixelDeltaFromAngleDelta(angleDelta) {
		return ((angleDelta / 8) / 15.0) * 20 * Qt.styleHints.wheelScrollLines
	}
	
	function calculateNewXPosition(wheel) {
		if ((flickable.contentWidth < flickable.width) || (wheel.pixelDelta.x === 0)) {
			return flickable.contentX
		}
		
		return scrollXByPixelDelta(wheel.pixelDelta.x)
	}
	
	function calculateNewYPosition(wheel) {
		if ((flickable.contentHeight < flickable.height) || (wheel.pixelDelta.y === 0 && wheel.angleDelta === 0)) {
			return flickable.contentY
		}
		
		if (wheel.angleDelta.y) {
			return scrollYByPixelDelta(pixelDeltaFromAngleDelta(wheel.angleDelta.y))
		} else {
			return scrollYByPixelDelta(wheel.pixelDelta.y)
		}
	}
	
	onWheel: {
		if (flickable.isBeingScrolled !== undefined) {
			flickable.isBeingScrolled = true
		}
		
		flickable.contentX = calculateNewXPosition(wheel)
		flickable.contentY = calculateNewYPosition(wheel)
	}
}
