"""
Anki Add-on

Copyright (c): 2020- ijgnd
               Ankitects Pty Ltd and contributors (filter_button.py)
               lovac42 (toolbar.py)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.



This add-on uses the file split_string.py which has this copyright and permission notice:

    Copyright (c): 2018  Rene Schallner
                   2020- ijgnd
        
    This file (split_string.py) is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This file is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this file.  If not, see <http://www.gnu.org/licenses/>.

"""

from aqt import mw
from aqt.gui_hooks import (
    browser_menus_did_init,
    profile_did_open,
)
from aqt.qt import (
    QAction,
    QKeySequence,
    QShortcut,
    qconnect,
)

from .config import gc
from .multi_line_dialog import SearchBox
from .toolbar import getMenu


alreadyrun = False
def quick_insert_addon_check():
    global alreadyrun
    global quick_insert_addon_filter_func
    if alreadyrun:
        return
    alreadyrun = True
    try:
        quick_insert_addon_filter_func = __import__("1052724801").onSearchEditTextChange
    except:
        quick_insert_addon_filter_func = None
profile_did_open.append(quick_insert_addon_check)



def open_multiline_searchwindow(browser):
    le = browser.form.searchEdit.lineEdit()
    sbi = SearchBox(browser, le.text(), quick_insert_addon_filter_func)
    if sbi.exec():
        le.setText(sbi.newsearch)
        le.setFocus()
        browser.onSearchActivated()


def setupBrowserShortcuts(self):
    # self is browser
    cut = gc("shortcut: open window")
    if cut:
       cm = QShortcut(QKeySequence(cut), self)
       qconnect(cm.activated, lambda b=self: open_multiline_searchwindow(b))
    view = getMenu(self, "&View")
    action = QAction(self)
    action.setText("Show search string in multi-line dialog")
    view.addAction(action)
    action.triggered.connect(lambda _, b=self: open_multiline_searchwindow(b))
browser_menus_did_init.append(setupBrowserShortcuts)
