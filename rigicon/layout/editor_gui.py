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

from wishlib import inside_softimage, inside_maya
from wishlib.qt import QtGui, QtCore, loadUiType, set_style

from rigicon.layout.library_gui import RigIconLibrary
from rigicon import library
from rigicon import icon

ui_file = os.path.join(os.path.dirname(__file__), "ui", "editor.ui")
form, base = loadUiType(ui_file)


class MPalette(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MPalette, self).__init__(parent)
        self._color = -1
        self._styleSheet = ""
        self.setupUi()
        for i, b in enumerate(self.buttons):
            self.setButtonColor(
                b, [x * 255 for x in pm.colorIndex(i + 1, q=True)])
            b.clicked.connect(lambda index=i + 1: self.accept(index))

    def setupUi(self):
        self.setWindowTitle("ColorPicker")
        self.gridLayout = QtGui.QGridLayout(self)
        self.buttons = list()
        for i in range(31):
            btn = QtGui.QPushButton(self)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                                           QtGui.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                btn.sizePolicy().hasHeightForWidth())
            btn.setSizePolicy(sizePolicy)
            btn.setMaximumSize(QtCore.QSize(25, 25))
            btn.setText(str(i + 1))
            self.gridLayout.addWidget(btn, int(i / 8), i % 8, 1, 1)
            self.buttons.append(btn)

    def setButtonColor(self, button, color):
        s = "background-color: rgb({0}, {1}, {2});".format(*color)
        button.setStyleSheet(s)

    def accept(self, index=None):
        self._color = index
        super(MPalette, self).accept()

    @classmethod
    def getColor(cls, parent):
        palette = cls(parent)
        palette.exec_()
        return palette._color


class RigIconEditorInterface(form, base):
    DEFAULT_VALUES = {"iconname_lineEdit": "",
                      "connect_label": "",
                      "shape_comboBox": 0,
                      "size_spinBox": 1.0,
                      "posx_spinBox": 0.0, "posy_spinBox": 0.0, "posz_spinBox": 0.0,
                      "rotx_spinBox": 0.0, "roty_spinBox": 0.0, "rotz_spinBox": 0.0,
                      "sclx_spinBox": 1.0, "scly_spinBox": 1.0, "sclz_spinBox": 1.0}

    def __init__(self, parent=None):
        super(RigIconEditorInterface, self).__init__(parent)
        self.setupUi(self)
        self.library_items = library.get_items()
        self.icons = list()
        self.multi = list()  # hold common multi selection values
        # func to set widget value by type
        self.set_type = {str: lambda widget, value: widget.setText(value),
                         bool: lambda widget, value: widget.setEnabled(value),
                         int: lambda widget, value: widget.setCurrentIndex(value),
                         float: lambda widget, value: widget.setValue(value),
                         list: lambda widget, value: self.set_color(value)}
        # fill gui values
        self.shape_comboBox.clear()
        self.shape_comboBox.addItem("Custom")
        for i in self.library_items:
            self.shape_comboBox.addItem(i.get("Name"))
        # connect signals
        self.reload_button.clicked.connect(self.reload_clicked)
        self.library_button.clicked.connect(self.library_clicked)
        self.color_button.clicked.connect(self.color_clicked)
        self.autoreload_checkBox.toggled.connect(self.autoreload_changed)
        self.shape_comboBox.currentIndexChanged.connect(self.shape_changed)
        self.connect_button.clicked.connect(self.connection_clicked)
        for spinbox in filter(lambda x: "_spinBox" in x, self.DEFAULT_VALUES.keys()):
            getattr(self, spinbox).editingFinished.connect(
                lambda y=spinbox: self.spinbox_changed(y))
        # connect selection events
        self.connect_selection()
        self.reload_clicked()

    # SLOTS
    def reload_clicked(self):
        pass

    def library_clicked(self):
        RigIconLibrary(parent=self).show()

    def color_clicked(self):
        # get color from stylesheet
        style = str(self.color_button.styleSheet())
        color = list(eval(style.split("rgb")[-1][:-1]))
        # launch color picker
        color_dialog = QtGui.QColorDialog(self)
        color_dialog.setCurrentColor(QtGui.QColor(*color))
        color_dialog.exec_()
        color = list(color_dialog.currentColor().getRgb())[:-1]
        self.set_color(color)

    def autoreload_changed(self, state):
        pass

    def spinbox_changed(self, widget_name):
        attr = widget_name.split("_")[0].lower()
        for x in self.icons:
            setattr(x, attr, getattr(self, widget_name).value())

    def shape_changed(self, index):
        index = index - 1
        if index < 0:
            return
        for rigicon in self.icons:
            rigicon.shape = self.library_items[index].get("Name")

    def connection_clicked(self):
        pass

    # HELPER FUNCTIONS
    def closeEvent(self, event):
        pass

    def connect_selection(self):
        pass

    def get_data(self):
        data = self.DEFAULT_VALUES.copy()
        self.multi = list()
        for index, rigicon in enumerate(self.icons):
            for k, v in data.iteritems():
                attr = k.split("_")[0]
                # get attr value
                if attr == "shape":
                    items = [i["Name"].lower() for i in self.library_items]
                    try:
                        value = items.index(rigicon.shape) + 1
                    except:
                        value = 0
                elif attr == "color":
                    #value = [rigicon.colorr, rigicon.colorg, rigicon.colorb]
                    #value = map(lambda x: int(x * 255), value)
                    pass
                elif attr == "connect":
                    value = str(rigicon.connect)
                else:
                    value = getattr(rigicon, attr)
                # filter multi-selection
                if index > 0:
                    if value != data.get(k):
                        value = self.DEFAULT_VALUES.get(k)
                        self.multi.append(k)
                # set multi-selection value
                data[k] = value
        return data

    def set_color(self, color):
        if "color_button" in self.multi:
            return
        # set color via stylesheet
        style = "background-color: rgb({0}, {1}, {2});".format(*color)
        self.color_button.setStyleSheet(style)
        # set rigicon color
        for rigicon in self.icons:
            for i, attr in enumerate(("colorr", "colorg", "colorb")):
                setattr(rigicon, attr, color[i] / 255.0)

if inside_softimage():
    from wishlib.si import si, sisel
    from sisignals import signals, muteSIEvent

    class RigIconEditor(RigIconEditorInterface):

        def reload_clicked(self):
            if sisel.Count:
                self.icons = [icon.Icon(x) for x in sisel if icon.is_icon(x)]
            # set widget values
            for key, value in self.get_data().iteritems():
                widget = getattr(self, key)
                function = self.set_type.get(type(value))
                # colorize multi widget
                style = ""
                if key in self.multi:
                    style = "background-color: rgb(35, 35, 35);"
                widget.setStyleSheet(style)
                # set widget values
                if function is not None:
                    function(widget, value)

        def library_clicked(self):
            si.Commands("RigIcon Library").Execute()

        def connection_clicked(self):
            picked = si.PickObject()("PickedElement")
            # set shape to every icon
            for each in self.icons:
                each.connect = picked
                self.connect_label.setText(str(picked))

        def autoreload_changed(self, state):
            muteSIEvent("siSelectionChange", not state)

        def closeEvent(self, event):
            muteSIEvent("siSelectionChange", True)
            self.close()

        def connect_selection(self):
            # connect siSelectionChange signal
            signals.siSelectionChange.connect(self.reload_clicked)
            bState = self.autoreload_checkBox.isChecked()
            muteSIEvent("siSelectionChange", not bState)

elif inside_maya():
    from wishlib.ma import show_qt
    import pymel.core as pm

    class RigIconEditor(RigIconEditorInterface):

        def __init__(self, parent):
            super(RigIconEditor, self).__init__(parent)

        def library_clicked(self):
            show_qt(RigIconLibrary)

        def reload_clicked(self):
            sel = pm.ls(selection=True)
            if sel:
                self.icons = [icon.Icon(x) for x in sel if icon.is_icon(x)]
                # set widget values
                for key, value in self.get_data().iteritems():
                    widget = getattr(self, key)
                    function = self.set_type.get(type(value))
                    # colorize multi widget
                    print self.multi
                    style = ""
                    if key in self.multi:
                        style = "background-color: rgb(35, 35, 35);"
                    widget.setStyleSheet(style)
                    # set widget values
                    if function is not None:
                        function(widget, value)

        def connection_clicked(self):
            sel = pm.ls(selection=True)
            if len(sel) == 1:
                # set shape to every icon
                for each in self.icons:
                    each.connect = sel[0]
                    self.connect_label.setText(str(sel[0]))
            if len(sel) == 0:
                # set shape to every icon
                for each in self.icons:
                    each.connect = None
                    self.connect_label.setText(str(None))

        def color_clicked(self):
            index = MPalette.getColor(parent=self)
            for icon in self.icons:
                icon.color = index

else:
    class RigIconEditor(RigIconEditorInterface):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = RigIconEditor()
    set_style(win, True)
    win.show()
    sys.exit(app.exec_())
