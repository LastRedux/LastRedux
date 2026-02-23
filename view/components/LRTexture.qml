import QtQuick
BorderImage{
	property string res
	property int xt:0
	property int xr:0
	property int xb:0
	property int xl:0
	anchors.fill:parent
	anchors.margins:-10
	source:'qrc:/sk_'+res+'.png'
	border.top:10+xt
	border.right:10+xr
	border.bottom:10+xb
	border.left:10+xl
}