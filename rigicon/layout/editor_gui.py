import os
from PyQt4 import uic, QtCore, QtGui
from sisignals import signals, muteSIEvent
from wishlib.si import si, sisel, log, C
from wishlib.qt import QDialog
from .. import icon
from .. import library


class GUI(QDialog):
    DEFAULT_VALUES = {"name_lineEdit": "",
                      "connLine_label": "",
                      "icons_comboBox": 0,
                      "priority_comboBox": 0,
                      "size_spinBox": 1.0,
                      "color_button": [0, 0, 0],
                      "posx_spinBox": 0.0,
                      "posy_spinBox": 0.0,
                      "posz_spinBox": 0.0,
                      "rotx_spinBox": 0.0,
                      "roty_spinBox": 0.0,
                      "rotz_spinBox": 0.0,
                      "sclx_spinBox": 1.0,
                      "scly_spinBox": 1.0,
                      "sclz_spinBox": 1.0,
                      "params_tabWidget": False}

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        uifile = os.path.join(os.path.dirname(__file__), "ui", "editor.ui")
        self.ui = uic.loadUi(os.path.normpath(uifile), self)
        # self._ConnectSignals()
        self.Reload_OnClicked()

    def Reload_OnClicked(self):
        # add icons from library
        self.ui.icons_comboBox.clear()
        self.ui.icons_comboBox.addItem("Custom")
        for i in library.items:
            self.ui.icons_comboBox.addItem(i.name)
        # set default values
        data_type = {str: lambda x, y: x.setText(y),
                     bool: lambda x, y: x.setEnabled(y),
                     int: lambda x, y: x.setCurrentIndex(y),
                     float: lambda x, y: x.setValue(y),
                     list: lambda x, y: self._setcolor(y)}
        for k, v in self.DEFAULT_VALUES.iteritems():
            f = data_type.get(type(v))
            f(getattr(self.ui, k), v)

    def Name_OnChanged(self):
        return
        name = str(self.ui.name_lineEdit.text())
        if len(self.lIcon) == 1:
            self.lIcon[0].SetName(name)
        elif len(self.lIcon) > 1:
            self.uiName_lineEdit.setText("MULTI")

    def Library_OnClicked(self):
        si.Commands("RigIconLibrary").Execute()

    def Color_OnClicked(self):
        style = str(self.ui.color_button.styleSheet())
        color = list(eval(style.split("rgb")[-1][:-1]))
        color_dialog = QtGui.QColorDialog(self)
        color_dialog.setCurrentColor(QtGui.QColor(*color))
        color_dialog.exec_()
        color = list(color_dialog.currentColor().getRgb())[:-1]
        self._setcolor(color)
        # color = map(lambda x: x / 255.0, color)
        # for i in self.lIcon:
            # i.wirecolorr = color[0]
            # i.wirecolorg = color[1]
            # i.wirecolorb = color[2]

    def Priority_OnChanged(self, p_iValue):
        return
        for i in self.lIcon:
            i.priority = float(p_iValue)

    def Icon_OnChanged(self, p_sIcon):
        return
        for i in self.lIcon:
            sIcon = str(i.icon)
            oItem = self.oLibrary.GetItemByName(str(p_sIcon))
            if oItem.GetName().lower() != sIcon.lower():
                i.icon = oItem.GetName()

    def SpinBox_OnChanged(self, p_sWidget):
        return
        sParam = p_sWidget[2:].split("_")[0].lower()
        for i in self.lIcon:
            setattr(i, sParam, getattr(self, p_sWidget).value())

    def Selection_OnChanged(self):
        return
        log("onSelectionChange event activated by csRigEditor", C.siVerbose)
        if self._GetActiveRigIcon():
            self.Reload_OnClicked()

    def LineTarget_OnClicked(self, sLabel=""):
        return
        oPick = si.PickElement(C.siObjectFilter)("PickedElement")
        if oPick:
            for i in self.lIcon:
                i.connect = oPick
        self.Reload_OnClicked()

    def Behaviour_OnChanged(self, p_iValue):
        return
        sBehaviour = ""
        if self.uiScaling_checkBox.isChecked():
            sBehaviour += "s"
        if self.uiRotation_checkBox.isChecked():
            sBehaviour += "r"
        if self.uiTranslation_checkBox.isChecked():
            sBehaviour += "t"
        for i in self.lIcon:
            i.behaviour = sBehaviour

    def Stylize_OnClicked(self):
        return
        for i in self.lIcon:
            i.Stylize(self.uiColor_checkBox.isChecked(),
                      self.uiIcon_checkBox.isChecked())

    def AutoRefresh_OnChanged(self, p_bState):
        return
        muteSIEvent("siSelectionChange", not p_bState)

    def closeEvent(self, event):
        return
        muteSIEvent("siSelectionChange", True)
        super(GUI, self).closeEvent(event)

    def _ConnectSignals(self):
        return
        # connect siSelectionChange signal
        signals.siSelectionChange.connect(self.Selection_OnChanged)
        bState = self.uiAutoReload_checkBox.isChecked()
        muteSIEvent("siSelectionChange", not bState)
        # connect spinbox signal
        for sSpinBox in filter(lambda x: "_spinBox" in x, self.DEFAULT_VALUES.keys()):
            oWidget = getattr(self, sSpinBox)
            func = lambda y=sSpinBox: self.SpinBox_OnChanged(y)
            QtCore.QObject.connect(oWidget,
                                   QtCore.SIGNAL("editingFinished()"),
                                   func)

    def _setcolor(self, p_lColor):
        sStyle = "background-color: rgb({0}, {1}, {2});".format(*p_lColor)
        self.ui.color_button.setStyleSheet(sStyle)

    def _GetActiveRigIcon(self):
        return
        lSel = map(lambda x: RigIcon(x), sisel)
        lSel = filter(lambda x: x.IsValid(), lSel)
        return lSel

    def _GetData(self, p_oIcon):
        return
        dData = self.DEFAULT_VALUES.copy()
        for sKey in dData.keys():
            oValue = None
            if "_spinBox" in sKey:
                oValue = getattr(p_oIcon, sKey[2:].split("_")[0].lower())
            elif "uiIcons_comboBox" in sKey:
                lItems = map(lambda x: x.GetName(), self.oLibrary.GetItems())
                try:
                    oValue = lItems.index(str(p_oIcon.icon)) + 1
                except:
                    oValue = 0  # set to custom
            elif "uiPriority_comboBox" in sKey:
                oValue = p_oIcon.priority
            elif "_lineEdit" in sKey:
                oValue = p_oIcon.GetName()
            elif "_button" in sKey:
                oValue = [
                    p_oIcon.wirecolorr, p_oIcon.wirecolorg, p_oIcon.wirecolorb]
                oValue = map(lambda x: int(x * 255), oValue)
            elif "_frame" in sKey:
                oValue = p_oIcon != None
            elif "_label" in sKey:
                oValue = str(p_oIcon.connect)
            dData[sKey] = oValue
        return dData
