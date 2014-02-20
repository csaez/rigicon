# This file is part of rigicon
# Copyright (C) 2014  Cesar Saez

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

from wishlib.qt import QtGui, QtCore, loadUi, widgets
from wishlib.si import sisel

from .. import library


class RigIconLibrary(widgets.QMainWindow):

    def __init__(self, parent=None):
        super(RigIconLibrary, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "library.ui")
        self.ui = loadUi(os.path.normpath(uifile), self)
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
        for curve in sisel:
            library.add_item(curve.Name, curve.ActivePrimitive.Geometry.Get2())
        self.Reload_OnClicked()

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
