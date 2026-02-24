#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QUrl>
int main(int argc,char* argv[]){
	#ifdef __APPLE__
		QQuickStyle::setStyle("macOS");
	#endif
	QGuiApplication app(argc,argv);
	app.setApplicationName("LastRedux");
	app.setQuitOnLastWindowClosed(false);
	qputenv("QML_DISABLE_DISTANCEFIELD","0");
	#ifdef __APPLE__
		qputenv("QML_DISABLE_DISTANCEFIELD","1");
	#elif defined(_WIN32)
		qputenv("QML_DISABLE_DISTANCEFIELD","1");
	#endif
	QQmlApplicationEngine engine;
	engine.load(QUrl("qrc:/view/Main.qml"));
	return app.exec();
}