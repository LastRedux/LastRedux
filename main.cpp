#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QUrl>
#include "src/LRViewModel.h"
int main(int argc,char* argv[]){
	#ifdef __APPLE__
		QQuickStyle::setStyle("macOS");
	#elif defined(_WIN32)
		QQuickStyle::setStyle("Windows");
	#else
		QQuickStyle::setStyle("Fusion");
	#endif
	qmlRegisterType<LRViewModel>("LastRedux",1,0,"LRViewModel");
	QGuiApplication app(argc,argv);
	app.setApplicationName("LastRedux");
	#ifdef __APPLE__
		app.setQuitOnLastWindowClosed(false);
		qputenv("QML_DISABLE_DISTANCEFIELD","1");
	#elif defined(_WIN32)
		qputenv("QML_DISABLE_DISTANCEFIELD","1");
	#else
		qputenv("QML_DISABLE_DISTANCEFIELD","0");
	#endif
	QQmlApplicationEngine engine;
	engine.load(QUrl("qrc:/view/Main.qml"));
	return app.exec();
}