import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Load the custom start page
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath("index.html")))

        self.search_engine_url = "https://www.google.com/search?q="

        # Navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Modified Home button with text
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Bookmarks toolbar
        self.bookmarks_toolbar = QToolBar("Bookmarks")
        self.addToolBar(Qt.LeftToolBarArea, self.bookmarks_toolbar)
        self.load_bookmarks()

        # Show the browser in maximized window mode
        self.showMaximized()

    def navigate_home(self):
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath("index.html")))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def load_bookmarks(self):
        # Load bookmarks from a file or define them here
        bookmarks = [
            ("Google", "https://www.google.com"),
            ("YouTube", "https://www.youtube.com"),
            ("GitHub", "https://www.github.com"),
            ("Driver Files", "http://driverfiles.ca/")
        ]
        for name, url in bookmarks:
            bookmark_action = QAction(name, self)
            bookmark_action.triggered.connect(lambda checked, url=url: self.browser.setUrl(QUrl(url)))
            self.bookmarks_toolbar.addAction(bookmark_action)

app = QApplication(sys.argv)
QApplication.setApplicationName("19cles Browser")
window = Browser()
app.exec_()
