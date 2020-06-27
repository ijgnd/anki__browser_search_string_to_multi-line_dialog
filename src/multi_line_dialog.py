from anki.utils import pointVersion

from aqt.qt import (
    QDialog,
    QTextCursor,
    Qt,
)

from aqt.utils import (
    restoreGeom,
    saveGeom,
)

from .filter_button import filter_button_cls
from .forms import search_box
from .split_string import split_to_multiline


class SearchBox(QDialog):
    def __init__(self, browser, searchstring, quick_insert_addon_filter_func):
        self.searchstring = searchstring
        self.parent = browser
        self.browser = browser
        QDialog.__init__(self, self.parent, Qt.Window)
        self.form = search_box.Ui_Dialog()
        self.form.setupUi(self)
        self.setupUI()
        self.settext()
        if quick_insert_addon_filter_func:
            self.quick_insert_addon_filter_func = quick_insert_addon_filter_func
            self.form.pte.textChanged.connect(self.text_change_helper)

    def setupUI(self):
        self.setWindowTitle("Anki: Search Term Multiline Window")
        self.resize(800, 350)
        restoreGeom(self, "BSMH")
        self.form.pb_accepted.clicked.connect(self.accept)
        self.form.pb_accepted.setShortcut("Ctrl+Return")
        self.form.pb_accepted.setToolTip("Ctrl+Return")
        self.form.pb_rejected.clicked.connect(self.reject)
        self.form.pb_rejected.setShortcut("Esc")
        self.form.pb_rejected.setToolTip("Esc")
        if pointVersion() >= 26:
            self.form.pb_filter.clicked.connect(self.filter_menu)
        else:
            # hide it
            self.form.pb_filter.setVisible(False)

    def filter_menu(self):
        func_gettext = self.form.pte.toPlainText
        func_settext = self.form.pte.setPlainText
        filter_button_cls(self, self.browser, func_gettext, func_settext)

    def settext(self):
        processed = split_to_multiline(self.searchstring)
        self.form.pte.setPlainText(processed)
        self.form.pte.setFocus()
        self.form.pte.moveCursor(QTextCursor.End)

    def process_text(self):
        text = self.form.pte.toPlainText()
        return text.replace("\n", "  ")

    def text_change_helper(self):
        parent = self.parent
        parent_is_browser = False
        func_gettext = self.form.pte.toPlainText
        func_settext = self.form.pte.setPlainText
        mw = self.browser.mw
        col = self.browser.col
        arg = self.form.pte.toPlainText()
        self.quick_insert_addon_filter_func(parent, parent_is_browser, func_gettext, func_settext, mw, col, arg)
        self.form.pte.moveCursor(QTextCursor.End)

    def reject(self):
        saveGeom(self, "BSMH")
        QDialog.reject(self)

    def accept(self):
        saveGeom(self, "BSMH")
        self.newsearch = self.process_text()
        QDialog.accept(self)
