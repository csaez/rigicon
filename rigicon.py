# Copyright (c) 2016 Cesar Saez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import OrderedDict
from PySide import QtGui
try:
    import maya.cmds as mc
except ImportError:
    pass

__all__ = ("library", "show", "create", "set", "append")


# ===============
# == GUI STUFF ==
# ===============
class QFlatButton(QtGui.QPushButton):
    def __init__(self, *args, **kwds):
        super(QFlatButton, self).__init__(*args, **kwds)
        self.setFlat(True)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum,
                           QtGui.QSizePolicy.Expanding)


class QVector3(QtGui.QWidget):
    def __init__(self, *args, **kwds):
        super(QVector3, self).__init__(*args, **kwds)
        self._widgets = list()

        layout = QtGui.QHBoxLayout()
        for axis in "xyz":
            w = QtGui.QDoubleSpinBox()
            self._widgets.append(w)
            setattr(self, axis, w)
            layout.addWidget(w)
        self.setLayout(layout)

        self.setMaximum(999)
        self.setMinimum(-999)
        self.setDecimals(3)
        self.setSingleStep(0.1)

    def setValue(self, values):
        for i, value in enumerate(values):
            self._widgets[i].setValue(value)

    def value(self):
        return [x.value() for x in self._widgets]

    def setMaximum(self, maximum):
        for x in self._widgets:
            x.setMaximum(maximum)

    def setMinimum(self, minimum):
        for x in self._widgets:
            x.setMinimum(minimum)

    def setSingleStep(self, step):
        for x in self._widgets:
            x.setSingleStep(step)

    def setDecimals(self, prec):
        for x in self._widgets:
            x.setDecimals(prec)


class LibraryWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(LibraryWidget, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        btnLayout = QtGui.QHBoxLayout()
        btnLayout.setSpacing(0)

        self.addBtn = QFlatButton("+")
        btnLayout.addWidget(self.addBtn)

        self.removeBtn = QFlatButton("-")
        btnLayout.addWidget(self.removeBtn)

        for btn in (self.addBtn, self.removeBtn):
            btn.setSizePolicy(QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding)

        layout.addLayout(btnLayout)

        self.iconList = QtGui.QListWidget()
        layout.addWidget(self.iconList)

        self.setLayout(layout)

    def addItem(self, text, description=None):
        libItem = LibraryWidgetItem(text)
        if description:
            libItem.setDescription(description)
        item = QtGui.QListWidgetItem()
        item.setSizeHint(libItem.sizeHint())
        self.iconList.addItem(item)
        self.iconList.setItemWidget(item, libItem)

        return item


class LibraryWidgetItem(QtGui.QWidget):
    def __init__(self, title, description=None, parent=None):
        super(LibraryWidgetItem, self).__init__(parent)

        self.setupUi()
        self.setTitle(title)
        self.setDescription(description)

    def setupUi(self):
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(0)

        self.title = QtGui.QLabel()
        titleFont = self.title.font()
        titleFont.setCapitalization(titleFont.AllUppercase)
        titleFont.setPointSize(16)
        self.title.setFont(titleFont)
        layout.addWidget(self.title)

        self.desc = QtGui.QLabel()
        descFont = self.desc.font()
        descFont.setItalic(True)
        descFont.setPointSize(8)
        self.desc.setFont(descFont)
        layout.addWidget(self.desc)

        self.setLayout(layout)

    def setTitle(self, text):
        self.title.setText(text)

    def setDescription(self, text=None):
        self.desc.setHidden(text is None)
        if text:
            self.desc.setText(text)


class RigIconDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        parent = parent or self.mainWindow()
        super(RigIconDialog, self).__init__(parent)
        self.setWindowTitle("RigIcon for Maya")
        self.setupUi()

        # fill library
        for item in library.items():
            self.library.addItem(item.name, item.description)

    def setupUi(self):
        layout = QtGui.QVBoxLayout()

        libGroup = QtGui.QGroupBox("Library")
        libLayout = QtGui.QVBoxLayout()
        self.library = LibraryWidget()
        libLayout.addWidget(self.library)
        libGroup.setLayout(libLayout)
        layout.addWidget(libGroup)

        offsetGroup = QtGui.QGroupBox("Offsets")

        offsetLayout = QtGui.QHBoxLayout()
        offsetLayout.setSpacing(0)

        offsetGridLayout = QtGui.QGridLayout()
        for i, label in enumerate(("translate", "rotate", "scale")):
            offsetGridLayout.addWidget(QtGui.QLabel(label.capitalize()), i, 0)
            widget = QVector3()
            offsetGridLayout.addWidget(widget, i, 1)
            setattr(self, label, widget)
        self.rotate.setSingleStep(5)
        self.scale.setValue([1, 1, 1])
        offsetLayout.addLayout(offsetGridLayout)

        self.offsetBtn = QFlatButton(">")
        self.offsetBtn.setFixedWidth(25)
        offsetLayout.addWidget(self.offsetBtn)

        offsetGroup.setLayout(offsetLayout)
        layout.addWidget(offsetGroup)

        self.setLayout(layout)

    @staticmethod
    def mainWindow():
        parent = QtGui.QApplication.activeWindow()
        if not parent:
            return None
        widget = parent.parent()
        while widget:
            parent = widget
            widget = parent.parent()
        return parent


# ================
# == PYTHON API ==
# ================
class LibraryItem(object):
    def __init__(self, name, description="", shapes=None):
        super(LibraryItem, self).__init__()
        self.name = name
        self.description = description
        self.shapes = shapes or list()

    def addShape(self, degree, point, knot=None):
        self.shapes.append({"degree": degree, "point": point, "knot": knot})

    @classmethod
    def fromMaya(cls, shapeNodes):
        data = LibraryItem.extractData(shapeNodes)
        item = cls(shapeNodes[0])
        for d in data:
            item.addShape(d["degree"], d["point"], d["knot"])
        return d

    @staticmethod
    def extractData(shapeNodes):
        if not isinstance(shapeNodes, (list, tuple)):
            shapeNodes = [shapeNodes]

        rval = list()
        toDelete = list()

        for shapeNode in shapeNodes:

            if mc.nodeType(shapeNode) == "transform":
                shapeNode = mc.listRelatives(shapeNode, shapes=True)

            data = dict()
            data["degree"] = mc.getAttr(shapeNode + ".degree")
            data["point"] = mc.getAttr(shapeNode + ".cv[*]")
            # knots
            curveInfo = mc.createNode("curveInfo")
            mc.connectAttr(shapeNode + ".worldSpace",
                           curveInfo + ".inputCurve")
            data["knot"] = mc.getAttr(curveInfo + ".knots[*]")

            rval.append(data)
            toDelete.append(curveInfo)

        mc.delete(toDelete)
        return rval


class Library(object):
    def __init__(self):
        super(Library, self).__init__()
        self._icons = OrderedDict()

        # add default item
        item = LibraryItem("square")
        item.description = ("Default library item... "
                            "feel free to add your own shapes, don't be shy!")
        item.addShape(degree=1,
                      point=[(-0.5, 0.0, 0.5), (0.5, 0.0, 0.5),
                             (0.5, 0.0, -0.5), (-0.5, 0.0, -0.5),
                             (-0.5, 0.0, 0.5)],
                      knot=[0.0, 1.0, 2.0, 3.0, 4.0])
        self.addItem(item)

    def list(self):
        return self._icons.keys()

    def add(self, name, shape):
        if isinstance(shape, basestring):
            shape = self.extractData(shape)
        self._icons[name] = shape

    def addItem(self, libraryItem):
        self._icons[libraryItem.name] = libraryItem

    def items(self):
        return self._icons.values()

    def remove(self, name):
        if self._icons.get(name):
            del self._icons[name]

    def default(self):
        return self._icons.keys()[0] if len(self._icons) else None

    def get(self, name):
        return self._icons.get(name)


def append(transformNode, icon=None, translate=None, rotate=None, scale=None):
    translate = translate or (0.0, 0.0, 0.0)
    rotate = rotate or (0.0, 0.0, 0.0)
    scale = scale or (1.0, 1.0, 1.0)

    if not icon or not library.get(icon):
        return False

    toDelete = list()
    for curveData in library.get(icon).shapes:
        curve = mc.curve(**curveData)
        shapes = mc.listRelatives(curve, shapes=True)
        mc.parent(shapes, transformNode, shape=True, relative=True)
        toDelete.append(curve)
    mc.delete(toDelete)

    return mc.listRelatives(transformNode, shapes=True)


def set(transformNode, icon=None, translate=None, rotate=None, scale=None):
    if icon:
        shapes = mc.listRelatives(transformNode, shapes=True)
        mc.delete(shapes)
    return append(transformNode, icon, translate, rotate, scale)


def create(name, icon=None, translate=None, rotate=None, scale=None):
    xfo = mc.createNode("transform", name=name)
    icon = icon or library.default()
    append(xfo, icon, translate, rotate, scale)
    return xfo


def show():
    d = RigIconDialog()
    d.show()


library = Library()  # singleton

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    d = RigIconDialog()
    d.show()
    sys.exit(app.exec_())
