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

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Menu bar for wallpaper change
        menubar = self.menuBar()
        viewMenu = menubar.addMenu('View')

        change_wallpaper_action = QAction('Change Wallpaper', self)
        change_wallpaper_action.triggered.connect(self.change_wallpaper)
        viewMenu.addAction(change_wallpaper_action)

        # Bookmarks toolbar
        self.bookmarks_toolbar = QToolBar("Bookmarks")
        self.addToolBar(Qt.LeftToolBarArea, self.bookmarks_toolbar)
        self.load_bookmarks()

        # Load saved wallpaper if it exists
        self.load_wallpaper()

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

    def change_wallpaper(self):
        # Open a file dialog to select an image file
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Image files (*.jpg *.jpeg *.png)"])
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.set_background_image(file_path)
            self.save_wallpaper(file_path)

    def set_background_image(self, image_path):
        # Set the selected image as the background of the main window
        image = QImage(image_path)
        if not image.isNull():
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(image))
            self.setPalette(palette)

    def save_wallpaper(self, image_path):
        with open("wallpaper_path.txt", "w") as file:
            file.write(image_path)

    def load_wallpaper(self):
        if os.path.exists("wallpaper_path.txt"):
            with open("wallpaper_path.txt", "r") as file:
                image_path = file.read()
                if os.path.exists(image_path):
                    self.set_background_image(image_path)

    def load_bookmarks(self):
        # Load bookmarks from a file or define them here
        bookmarks = [
            ("Google", "https://www.google.com"),
            ("YouTube", "https://www.youtube.com"),
            ("GitHub", "https://www.github.com")
        ]
        for name, url in bookmarks:
            bookmark_action = QAction(name, self)
            bookmark_action.triggered.connect(lambda checked, url=url: self.browser.setUrl(QUrl(url)))
            self.bookmarks_toolbar.addAction(bookmark_action)

app = QApplication(sys.argv)
QApplication.setApplicationName("19cles Browser")
window = Browser()
app.exec_()
