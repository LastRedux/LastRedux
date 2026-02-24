cmake_minimum_required(VERSION 3.16)
project(LastRedux VERSION 1.0)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(BIN ${CMAKE_CURRENT_BINARY_DIR})
set(_ ${CMAKE_CURRENT_SOURCE_DIR})


#Qt
if(APPLE)
	set(CMAKE_MACOSX_RPATH ON)
	set(CMAKE_INSTALL_RPATH_USE_LINK_PATH OFF)
	set(CMAKE_BUILD_RPATH_USE_ORIGIN ON)
	file(GLOB QTPATHS "$ENV{HOME}/Qt/6.*/macos")
	list(SORT QTPATHS COMPARE NATURAL ORDER DESCENDING)
	foreach(QTPATH IN LISTS QTPATHS)
		if(EXISTS "${QTPATH}/lib/cmake/Qt6")
			set(CMAKE_PREFIX_PATH "${CMAKE_PREFIX_PATH};${QTPATH}" CACHE PATH "Qt")
			break()
		endif()
	endforeach()
endif()


#Resources
file(GLOB RESDIR CONFIGURE_DEPENDS "${_}/res/*.png")
set(RES "")
foreach(RESFILE ${RESDIR})
	get_filename_component(RESNAME ${RESFILE} NAME)
	string(APPEND RES "\t\t<file alias=\"${RESNAME}\">${RESFILE}</file>\n")
endforeach()
configure_file(
	${_}/cmake/res.qrc.in
	${BIN}/res.qrc
	@ONLY
)


#QML
file(GLOB_RECURSE QMLDIR CONFIGURE_DEPENDS "${_}/view/*.qml")
set(QML "")
foreach(QMLFILE ${QMLDIR})
	get_filename_component(QMLNAME ${QMLFILE} NAME)
	string(APPEND QML "\t\t<file alias=\"${QMLNAME}\">${QMLFILE}</file>\n")
endforeach()
configure_file(
	${_}/cmake/qml.qrc.in
	${BIN}/qml.qrc
	@ONLY
)


#Sources
set(SRC
	src/main.cpp
	${BIN}/qml.qrc
)


#Target
add_executable(LastRedux MACOSX_BUNDLE ${SRC} ${CMAKE_CURRENT_BINARY_DIR}/res.qrc)
set(CMAKE_FIND_FRAMEWORK LAST)
set(CMAKE_FIND_APPBUNDLE LAST)
target_compile_options(LastRedux PRIVATE -O3 -Wall -Wextra)
if(APPLE)
	target_compile_options(LastRedux PRIVATE -flto=full)
	target_link_options(LastRedux PRIVATE -flto=full -Wl,-dead_strip)
else()
	target_compile_options(LastRedux PRIVATE -fdata-sections -ffunction-sections -flto)
	target_link_options(LastRedux PRIVATE -flto -Wl,--gc-sections)
	target_link_libraries(LastRedux PRIVATE stdc++)
endif()
find_package(Qt6 6.2 COMPONENTS Core Network Quick QuickControls2 LabsPlatform QUIET)
target_link_libraries(LastRedux PRIVATE
	Qt6::Core
	Qt6::Network
	Qt6::Quick
	Qt6::QuickControls2
	Qt6::LabsPlatform
)


#Deploy/Mac
if(APPLE)
	get_target_property(QMAKE Qt6::qmake IMPORTED_LOCATION)
	get_filename_component(QTBIN "${QMAKE}" DIRECTORY)
	find_program(QDEPLOY macdeployqt HINTS "${QTBIN}")
	set_target_properties(LastRedux PROPERTIES
		MACOSX_BUNDLE_GUI_IDENTIFIER com.firstam.client
		MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
		MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION}
		MACOSX_BUNDLE_BUNDLE_NAME "LastRedux"
		MACOSX_BUNDLE_INFO_STRING "LastRedux"
		MACOSX_BUNDLE_INFO_PLIST "${_}/src/platform/Info.plist"
		INSTALL_RPATH "@executable_path/../Frameworks;@loader_path/../Frameworks"
		INSTALL_RPATH_USE_LINK_PATH OFF
		BUILD_RPATH_USE_ORIGIN ON
		MACOSX_RPATH ON
	)
	if(QDEPLOY)
		add_custom_command(TARGET LastRedux POST_BUILD
			COMMAND bash "${_}/cmake/deploy.sh" "${BIN}" "${QDEPLOY}" "${_}/view"
		)
	else()
		message(STATUS "macdeployqt not found")
	endif()
endif()


#Install
install(TARGETS LastRedux
	BUNDLE DESTINATION .
	RUNTIME DESTINATION bin
)
