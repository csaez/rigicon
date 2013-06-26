import os
from PyQt4 import uic, QtCore, QtGui
from sisignals import signals, muteSIEvent
from wishlib.si import si, sisel
from wishlib.qt.QtGui import QDialog
from .. import icon
from .. import library


class RigIconEditor(QDialog):
    DEFAULT_VALUES = {"iconname_lineEdit": "",
                      "connect_label": "",
                      "shape_comboBox": 0,
                      "size_spinBox": 1.0,
                      "color_button": [0, 0, 0],
                      "posx_spinBox": 0.0, "posy_spinBox": 0.0, "posz_spinBox": 0.0,
                      "rotx_spinBox": 0.0, "roty_spinBox": 0.0, "rotz_spinBox": 0.0,
                      "sclx_spinBox": 1.0, "scly_spinBox": 1.0, "sclz_spinBox": 1.0}

    def __init__(self, parent=None):
        super(RigIconEditor, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "editor.ui")
        self.ui = uic.loadUi(os.path.normpath(uifile), self)
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
        self.ui.shape_comboBox.clear()
        self.ui.shape_comboBox.addItem("Custom")
        for i in self.library_items:
            self.ui.shape_comboBox.addItem(i.name)
        # connect signals and load values using selection
        self._connect_signals()
        self.reload_clicked()

    # SLOTS
    def reload_clicked(self):
        if sisel.Count:
            self.icons = [icon.Icon(x) for x in sisel if icon.is_icon(x)]
        # set widget values
        for key, value in self.get_data().iteritems():
            widget = getattr(self.ui, key)
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
        si.Commands("RigIconLibrary").Execute()

    def color_clicked(self):
        # get color from stylesheet
        style = str(self.ui.color_button.styleSheet())
        color = list(eval(style.split("rgb")[-1][:-1]))
        # launch color picker
        color_dialog = QtGui.QColorDialog(self)
        color_dialog.setCurrentColor(QtGui.QColor(*color))
        color_dialog.exec_()
        color = list(color_dialog.currentColor().getRgb())[:-1]
        self.set_color(color)

    def autoreload_changed(self, state):
        muteSIEvent("siSelectionChange", not state)

    def spinbox_changed(self, widget_name):
        attr = widget_name.split("_")[0].lower()
        for i in self.icons:
            setattr(i, attr, getattr(self, widget_name).value())

    def shape_changed(self, index):
        index = index - 1
        if index < 0:
            return
        for rigicon in self.icons:
            rigicon.shape = self.library_items[index].name

    def connection_clicked(self):
        picked = si.PickObject()("PickedElement")
        # set shape to every icon
        for each in self.icons:
            each.connect = picked
            self.ui.connect_label.setText(str(picked))

    # HELPER FUNCTIONS
    def closeEvent(self, event):
        muteSIEvent("siSelectionChange", True)
        self.close()

    def _connect_signals(self):
        # connect siSelectionChange signal
        signals.siSelectionChange.connect(self.reload_clicked)
        bState = self.ui.autoreload_checkBox.isChecked()
        muteSIEvent("siSelectionChange", not bState)
        # connect spinbox signal
        for spinbox in filter(lambda x: "_spinBox" in x, self.DEFAULT_VALUES.keys()):
            widget = getattr(self, spinbox)
            QtCore.QObject.connect(widget, QtCore.SIGNAL("editingFinished()"),
                                   lambda y=spinbox: self.spinbox_changed(y))

    def get_data(self):
        data = self.DEFAULT_VALUES.copy()
        self.multi = list()
        for index, icon in enumerate(self.icons):
            for k, v in data.iteritems():
                attr = k.split("_")[0]
                # get attr value
                if attr == "shape":
                    items = [i.name.lower() for i in self.library_items]
                    value = items.index(icon.shape) + 1
                elif attr == "color":
                    value = [icon.colorr, icon.colorg, icon.colorb]
                    value = map(lambda x: int(x * 255), value)
                elif attr == "connect":
                    value = str(icon.connect)
                else:
                    value = getattr(icon, attr)
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
        self.ui.color_button.setStyleSheet(style)
        # set rigicon color
        for rigicon in self.icons:
            for i, attr in enumerate(("colorr", "colorg", "colorb")):
                setattr(rigicon, attr, color[i] / 255.0)
