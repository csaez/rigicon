# This file is part of rigicon
# Copyright (C) 2014 Cesar Saez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from wishlib import inside_maya, inside_softimage
from wishlib.qt import QtGui, QtCore, loadUi, set_style
from rigicon import library


class RigIconLibraryInferface(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(RigIconLibraryInferface, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "library.ui")
        self.ui = loadUi(os.path.normpath(uifile), self)
        # signals
        self.ui.add_button.clicked.connect(self.Add_OnClicked)
        self.ui.remove_button.clicked.connect(self.Remove_OnClicked)
        self.ui.reload_button.clicked.connect(self.Reload_OnClicked)
        self.ui.items_listWidget.itemChanged.connect(self.Rename_OnChanged)
        # load items
        self.Reload_OnClicked()

    def Reload_OnClicked(self):
        self.ui.items_listWidget.clear()
        for library_item in library.get_items():
            item = QtGui.QListWidgetItem(library_item.get("Name"))
            item.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsEditable |
                          QtCore.Qt.ItemIsEnabled)
            self.ui.items_listWidget.addItem(item)

    def Add_OnClicked(self):
        pass

    def Remove_OnClicked(self):
        selected = str(self.ui.items_listWidget.currentItem().text())
        library.remove_item(selected)
        self.Reload_OnClicked()

    def Rename_OnChanged(self, item):
        index = self.ui.items_listWidget.currentRow()
        item = [i for i in library.get_items()][index]
        new_name = str(self.ui.items_listWidget.currentItem().text())
        library.rename_item(item, new_name)
        self.Reload_OnClicked()

if inside_softimage():
    from wishlib.si import sisel

    class RigIconLibrary(RigIconLibraryInferface):

        def Add_OnClicked(self):
            for curve in sisel:
                data = curve.ActivePrimitive.Geometry.Get2()
                library.add_item(curve.Name, data)
            self.Reload_OnClicked()

elif inside_maya():
    class RigIconLibrary(RigIconLibraryInferface):

        def Add_OnClicked(self):
            pass

else:
    class RigIconLibrary(RigIconLibraryInferface):

        def __init__(self, *args, **kargs):
            super(RigIconLibrary, self).__init__(*args, **kargs)
            self.ui.add_button.setDisabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = RigIconLibrary()
    set_style(win, True)
    win.show()
    sys.exit(app.exec_())
