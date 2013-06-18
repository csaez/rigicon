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
                      "color_button": [0, 0, 0],
                      "shape_comboBox": 0,
                      "priority_comboBox": 0,
                      "size_spinBox": 1.0,
                      "posx_spinBox": 0.0,
                      "posy_spinBox": 0.0,
                      "posz_spinBox": 0.0,
                      "rotx_spinBox": 0.0,
                      "roty_spinBox": 0.0,
                      "rotz_spinBox": 0.0,
                      "sclx_spinBox": 1.0,
                      "scly_spinBox": 1.0,
                      "sclz_spinBox": 1.0,
                      "params_tabWidget": True}

    def __init__(self, parent=None):
        super(RigIconEditor, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "editor.ui")
        self.ui = uic.loadUi(os.path.normpath(uifile), self)
        self.set_type = {str: lambda widget, value: widget.setText(value),
                         bool: lambda widget, value: widget.setEnabled(value),
                         int: lambda widget, value: widget.setCurrentIndex(value),
                         float: lambda widget, value: widget.setValue(value),
                         list: lambda widget, value: self.set_color(value)}
        self.icons = list()
        self._connect_signals()
        self.reload_clicked(True)

    def reload_clicked(self, reload_library=False):
        if reload_library:
            self.ui.shape_comboBox.clear()
            self.ui.shape_comboBox.addItem("Custom")
            for i in library.get_items():
                self.ui.shape_comboBox.addItem(i.name)
        # set widget values
        values = self.DEFAULT_VALUES.copy()
        for k, v in values.iteritems():
            function = self.set_type.get(type(v))
            if function is not None:
                widget = getattr(self.ui, k)
                function(widget, v)

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

    def set_color(self, color):
        # set color via stylesheet
        style = "background-color: rgb({0}, {1}, {2});".format(*color)
        self.ui.color_button.setStyleSheet(style)

    def autoreload_changed(self, p_bState):
        muteSIEvent("siSelectionChange", not p_bState)

    def closeEvent(self, event):
        muteSIEvent("siSelectionChange", True)
        super(RigIconEditor, self).closeEvent(event)

    def _connect_signals(self):
        # connect siSelectionChange signal
        # signals.siSelectionChange.connect(self.reload_clicked)
        # bState = self.ui.autoreload_checkBox.isChecked()
        # muteSIEvent("siSelectionChange", not bState)
        # connect spinbox signal
        for spinbox in filter(lambda x: "_spinBox" in x, self.DEFAULT_VALUES.keys()):
            widget = getattr(self, spinbox)
            QtCore.QObject.connect(widget, QtCore.SIGNAL("editingFinished()"),
                                   lambda y=spinbox: self.spinbox_changed(y))

    def spinbox_changed(self, widget_name):
        attr = widget_name.split("_")[0].lower()
        for i in self.icons:
            setattr(i, attr, getattr(self, widget_name).value())

    def get_icons(self):
        self.icons = list()
        for x in sisel:
            if icon.is_icon(x):
                self.icons.append(icon.Icon(x))
        return self.icons
