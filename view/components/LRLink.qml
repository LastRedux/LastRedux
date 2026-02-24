import QtQuick
import Qt.labs.platform
Item{
	property string href:''
	property string content:''
	property bool enabled:true
	property bool hovered:mEnabled&&xHover.hovered
	property bool pressed:mEnabled&&(mMenuShow||(!mMenuShow&&xMouse.containsPress))
	property bool mEnabled:enabled&&href
	property alias mHook:xRoot.parent
	property bool mHasLabel:mHook.font!==undefined
	property string mContent:(content!==''?content:(mHasLabel?mHook.content:content)).trim()
	property string mEngineLink:'https://www.google.com/search?q='
	property bool mMenuShow:false
	property bool mCanLookup:Qt.platform.os==='osx'&&mContent
	signal clicked
	id:xRoot
	width:mHasLabel?mHook.contentWidth:mHook.width
	height:mHasLabel?mHook.contentHeight:mHook.height
	states:[
		State{
			when:mHasLabel&&hovered&&pressed
			PropertyChanges{
				target:mHook
				font.underline:true
				alphaMod:0.5
			}
		},
		State{
			when:mHasLabel&&hovered
			PropertyChanges{
				target:mHook
				font.underline:true
			}
		}
	]
	TextInput{
		id:xCopy
		visible:false
	}
	HoverHandler{
		id:xHover
		cursorShape:mHasLabel&&mEnabled?Qt.PointingHandCursor:Qt.ArrowCursor
	}
	MouseArea{
		id:xMouse
		anchors.fill:parent
		acceptedButtons:Qt.LeftButton|Qt.RightButton
		focusPolicy:Qt.NoFocus
		enabled:!mMenuShow
		visible:!mMenuShow
		onClicked:function(mouse){
			if(mouse.button!==Qt.LeftButton)return
			xRoot.clicked()
			if(href)Qt.openUrlExternally(href)
		}
		onPressed:function(mouse){
			if(!active||mouse.button!==Qt.RightButton)return
			if(mCanLookup){
				var cropped=mContent
				if(cropped.length>30)cropped=cropped.substring(0,30).trim()+'...'
				xLookup.text='Look Up "'+cropped+'"'
			}
			menu.open()
		}
	}
	Menu{
		id:menu
		onAboutToShow:mMenuShow=true
		onAboutToHide:mMenuShow=false
		MenuItem{
			enabled:mEnabled
			visible:href
			text:'Open Link'
			onTriggered:{
				if(!mEnabled||!href)return
				Qt.openUrlExternally(href)
			}
		}
		MenuItem{
			enabled:mEnabled
			visible:href
			text:'Copy Link'
			onTriggered:{
				if(!mEnabled||!href)return
				xCopy.text=href
				xCopy.selectAll()
				xCopy.copy()
			}
		}
		MenuSeparator{visible:href&&mContent}
		MenuItem{
			id:xLookup
			enabled:mCanLookup
			visible:mCanLookup
			onTriggered:{
				if(!mCanLookup)return
				Qt.openUrlExternally(mEngineLink+encodeURIComponent(mContent))
			}
		}
		MenuSeparator{visible:Qt.platform.os==='osx'&&mContent}
		MenuItem{enabled:false;text:'Cut'}
		MenuItem{
			enabled:mContent
			text:'Copy'
			onTriggered:{
				if(!mContent)return
				xCopy.text=mContent
				xCopy.selectAll()
				xCopy.copy()
			}
		}
		MenuItem{enabled:false;text:'Paste'}
	}
}