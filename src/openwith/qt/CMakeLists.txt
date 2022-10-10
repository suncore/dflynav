cmake_minimum_required(VERSION 3.0)

project (openwith)

set(QT_MIN_VERSION "5.3.0")
set(KF5_MIN_VERSION "5.2.0")

find_package(ECM 1.0.0 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)
include(FeatureSummary)

# Find Qt modules
find_package(Qt5 ${QT_MIN_VERSION} CONFIG REQUIRED COMPONENTS
    Core    # QCommandLineParser, QStringLiteral
    Widgets # QApplication
)

# Find KDE modules
find_package(KF5 ${KF5_MIN_VERSION} REQUIRED COMPONENTS
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
    Qt5::Widgets
    KF5::CoreAddons
    KF5::I18n
    KF5::WidgetsAddons
    KF5::XmlGui
    KF5::TextWidgets
    KF5::KIOCore 
    KF5::KIOFileWidgets 
    KF5::KIOWidgets 
    KF5::KIONTLM
)

install(TARGETS openwith ${KDE_INSTALL_TARGETS_DEFAULT_ARGS})
