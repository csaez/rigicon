import os
from PyQt4 import uic, QtCore, QtGui
from wishlib.qt import QMainWindow
from wishlib.si import sisel
from .. import library


class GUI(QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "library.ui")
        self.ui = uic.loadUi(os.path.normpath(uifile), self)
        self.Reload_OnClicked()

    def Reload_OnClicked(self):
        self.ui.items_listWidget.clear()
        for library_item in library.items:
            item = QtGui.QListWidgetItem(library_item.name)
            item.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsEditable |
                          QtCore.Qt.ItemIsEnabled)
            self.ui.items_listWidget.addItem(item)

    def Add_OnClicked(self):
        for curve in sisel:
            library_item = library.LibraryItem(curve.Name)
            library_item.data = curve.ActivePrimitive.Geometry.Get2()
            library.items.append(library_item)
        self.Reload_OnClicked()

    def Remove_OnClicked(self):
        selected = str(self.ui.items_listWidget.currentItem().text())
        for i, library_item in enumerate(library.items):
            if library_item.name != selected:
                continue
            library_item.remove()
            library.items.pop(i)
        self.Reload_OnClicked()

    def Rename_OnChanged(self, item):
        index = self.ui.items_listWidget.currentRow()
        item = library.items[index]
        item.name = str(self.ui.items_listWidget.currentItem().text())
        self.Reload_OnClicked()
