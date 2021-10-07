#include <QApplication>
#include <KMessageBox>
#include <KAboutData>
#include <KLocalizedString>
#include <QCommandLineParser>
#include <KTextEdit>
#include <KXmlGuiWindow>
#include <KIO/ApplicationLauncherJob>
#include <KIO/JobUiDelegate>

class KTextEdit;
 
class MainWindow : public KXmlGuiWindow
{
public:
    explicit MainWindow(QWidget *parent = nullptr);
 
private:
    KTextEdit *textArea;
};
 
MainWindow::MainWindow(QWidget *parent) : KXmlGuiWindow(parent)
{
    textArea = new KTextEdit();
    setCentralWidget(textArea);
    setupGUI();
}

int main (int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr,"Usage: %s <file_to_open>\n",argv[0]);
        return 0;
    }
    QApplication app(argc, argv);
    KLocalizedString::setApplicationDomain("Dragonfly");
    
    KAboutData aboutData(
                         // The program name used internally. (componentName)
                         QStringLiteral("Dragonfly"),
                         // A displayable program name string. (displayName)
                         i18n("Dragonfly"),
                         // The program version string. (version)
                         QStringLiteral("1.0"),
                         // Short description of what the app does. (shortDescription)
                         i18n("Dragonfly KDE openwith dialog"),
                         // The license this code is released under
                         KAboutLicense::GPL,
                         // Copyright Statement (copyrightStatement = QString())
                         i18n("(c) 2021"),
                         // Optional text shown in the About box.
                         // Can contain any information desired. (otherText)
                         i18n(""),
                         // The program homepage string. (homePageAddress = QString())
                         QStringLiteral("https://github.com/suncore/dflynav"),
                         // The bug report email address
                         // (bugsEmailAddress = QLatin1String("submit@bugs.kde.org")
                         QStringLiteral(""));


    KAboutData::setApplicationData(aboutData);

    QCommandLineParser parser;
    aboutData.setupCommandLine(&parser);
    parser.process(app);
    aboutData.processCommandLine(&parser);
    MainWindow *window = new MainWindow();
    auto *job = new KIO::ApplicationLauncherJob();
    auto url = argv[1];
    job->setUrls({QUrl(url)});
    job->setUiDelegate(new KIO::JobUiDelegate(KJobUiDelegate::AutoHandlingEnabled, window));
    //window->show();
    job->start();
    window->close();
    return app.exec();
}
