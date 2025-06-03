import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup browser
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Theme flags
        self.is_dark_mode = False

        # Load initial home page
        self.navigate_home()

        # NavBar
        navbar = QToolBar()
        navbar.setIconSize(QSize(20, 20))
        navbar.setMovable(False)
        self.addToolBar(navbar)

        back_btn = QAction('👈', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('👉', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('🔄️', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Search with Khu")
        self.url_bar.returnPressed.connect(self.khu_search)
        navbar.addWidget(self.url_bar)

        theme_btn = QAction('🌙', self)
        theme_btn.triggered.connect(self.toggle_theme)
        navbar.addAction(theme_btn)

        self.browser.urlChanged.connect(self.update_url)

        # Apply light theme initially
        self.apply_light_theme()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def khu_search(self):
        text = self.url_bar.text()
        if text.startswith("http://") or text.startswith("https://"):
            url = text
        elif "." in text:
            url = "http://" + text
        else:
            url = f"https://www.google.com/search?q={text}"
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def toggle_theme(self):
        if self.is_dark_mode:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.is_dark_mode = not self.is_dark_mode

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QToolBar {
                background-color: #ffffff;
                spacing: 10px;
                padding: 8px;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                padding: 6px;
                border-radius: 8px;
                min-width: 400px;
                font-size: 14px;
            }
        """)
        self.set_browser_background("#ffffff", "#000000")

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QToolBar {
                background-color: #1e1e1e;
                spacing: 10px;
                padding: 8px;
            }
            QLineEdit {
                background-color: #2c2c2c;
                color: #ffffff;
                padding: 6px;
                border-radius: 8px;
                min-width: 400px;
                font-size: 14px;
            }
        """)
        self.set_browser_background("#121212", "#ffffff")

    def set_browser_background(self, bg_color, text_color):
        # Inject CSS into every page
        css = f"""
            body {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
        """
        script = QWebEngineScript()
        script.setSourceCode(f"""
            var style = document.createElement('style');
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
        """)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.MainWorld)

        self.browser.page().scripts().clear()  # remove previous themes
        self.browser.page().scripts().insert(script)

        # Refresh page to apply theme
        self.browser.reload()


app = QApplication(sys.argv)
QApplication.setApplicationName("Khu Browser")
window = MainWindow()
app.exec_()
