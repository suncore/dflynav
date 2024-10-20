cmake_minimum_required(VERSION 3.30)

project (openwith)

set(QT_MIN_VERSION "6.0.0")
set(KF6_MIN_VERSION "6.0.0")

find_package(ECM 1.0.0 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)
include(FeatureSummary)

# Find Qt modules
find_package(Qt6 ${QT_MIN_VERSION} CONFIG REQUIRED COMPONENTS
    Core    # QCommandLineParser, QStringLiteral
    Widgets # QApplication
)

# Find KDE modules
find_package(KF6 ${KF6_MIN_VERSION} REQUIRED COMPONENTS
    CoreAddons      # KAboutData
    I18n            # KLocalizedString
    WidgetsAddons   # KMessageBox
    XmlGui          # KXmlGuiWindow
    TextWidgets     # KTextEdit
    KIO
)

set(openwith_SRCS main.cpp)
add_executable(openwith ${openwith_SRCS})
target_link_libraries(openwith
    Qt6::Widgets
    KF6::CoreAddons
    KF6::I18n
    KF6::WidgetsAddons
    KF6::XmlGui
    KF6::TextWidgets
    KF6::KIOCore 
    KF6::KIOFileWidgets 
    KF6::KIOWidgets 
)

install(TARGETS openwith ${KDE_INSTALL_TARGETS_DEFAULT_ARGS})
