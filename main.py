"""Implementation based on https://stackoverflow.com/a/66067392/1939934"""

import sleap
import sleap.gui.web

import os

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Property, Signal, QObject, QUrl
from qtpy.QtWebChannel import QWebChannel
from qtpy.QtWebEngineWidgets import QWebEngineView


class Document(QObject):
    textChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_text = ""

    def get_text(self):
        return self.m_text

    def set_text(self, text):
        if self.m_text == text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    text = Property(str, fget=get_text, fset=set_text, notify=textChanged)


if __name__ == "__main__":
    release_checker = sleap.gui.web.ReleaseChecker()
    release_checker.check_for_releases()
    rls = release_checker.latest_release
    print(rls.description)

    # Last releases
    release_markdown = "-----\n".join(
        [
            "# " + rls.title + "\n" + rls.description
            for rls in release_checker.releases[:10]
        ]
    )

    app = QApplication([])

    document = Document()
    channel = QWebChannel()
    channel.registerObject("content", document)

    document.set_text(release_markdown)

    view = QWebEngineView()
    view.page().setWebChannel(channel)
    filename = os.path.dirname(os.path.realpath(__file__)) + "/markdown.html"
    url = QUrl.fromLocalFile(filename)
    view.load(url)
    view.resize(640, 480)
    view.show()

    app.exec_()
