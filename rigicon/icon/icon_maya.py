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

from .. import library

import wishlib.ma as app
reload(app)

DEFAULT_DATA = {"size": 1.0, "shape": "Null", "connect": None,
                "colorr": 1.0, "colorg": 0.882, "colorb": 0.0,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0,
                "sizex": 1.0, "sizey": 1.0, "sizez": 1.0}
DATA_LINK = "RigIcon_Data"


def is_icon(obj):
    if obj.Type == "curve" and obj.Attributes(DATA_LINK):
        return True
    return False


class Icon(app.Wrapper):

    @classmethod
    def create(cls, name="rigicon", **options):
        obj = app.createCurve()
        obj.Name = name
        icon = cls(obj)
        for k, v in options.iteritems():
            if hasattr(icon, k):
                setattr(icon, k, v)
        return icon

    @classmethod
    def new(cls, *args, **kwds):
        return cls.create(*args, **kwds)

    def __new__(cls, obj):
        if isinstance(obj, str):
            obj = app.Object(obj)

        if obj.Type == "curve":
            return app.Wrapper.__new__(cls, obj)
        print "ERROR:", obj, "type isnt an icon object."

    def __init__(self, obj):

        #adding exceptions for class properties
        exceptions = ['connect', 'size', 'connect_line',
                      'shape', "posx", "posy", "posz",
                      "rotx", "roty", "rotz",
                      "sclx", "scly", "sclz",
                      "sizex", "sizey", "sizez"]

        for e in exceptions:
            self.EXCEPTIONS.append(e)

        #case of passing in a string
        if isinstance(obj, str):
            obj = app.Object(obj)

        super(Icon, self).__init__(obj, DATA_LINK)
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

    def _returnAttr(self, attr, value=0.0):
        if not hasattr(self, '_' + attr):
            setattr(self, '_' + attr, value)
        return getattr(self, '_' + attr)

    @property
    def posx(self):
        return self._returnAttr('posx')

    @posx.setter
    def posx(self, value):
        self.Translate((self.posx * -1), 0, 0)
        self.Translate(value, 0, 0)
        self._posx = value

    @property
    def posy(self):
        return self._returnAttr('posy')

    @posy.setter
    def posy(self, value):
        self.Translate(0, (self.posy * -1), 0)
        self.Translate(0, value, 0)
        self._posy = value

    @property
    def posz(self):
        return self._returnAttr('posz')

    @posz.setter
    def posz(self, value):
        self.Translate(0, 0, (self.posz * -1))
        self.Translate(0, 0, value)
        self._posz = value

    @property
    def rotx(self):
        return self._returnAttr('rotx')

    @rotx.setter
    def rotx(self, value):
        self.Rotate((self.rotx * -1), 0, 0)
        self.Rotate(value, 0, 0)
        self._rotx = value

    @property
    def roty(self):
        return self._returnAttr('roty')

    @roty.setter
    def roty(self, value):
        self.Rotate(0, (self.roty * -1), 0)
        self.Rotate(0, value, 0)
        self._roty = value

    @property
    def rotz(self):
        return self._returnAttr('rotz')

    @rotz.setter
    def rotz(self, value):
        self.Rotate(0, 0, (self.rotz * -1))
        self.Rotate(0, 0, value)
        self._rotz = value

    @property
    def sizex(self):
        return self._returnAttr('sizex', 1)

    @sizex.setter
    def sizex(self, value):
        self.Scale(1.0 / self.sizex, 1, 1)
        self.Scale(value, 1, 1)
        self._sizex = value

    @property
    def sizey(self):
        return self._returnAttr('sizey', 1)

    @sizey.setter
    def sizey(self, value):
        self.Scale(1, 1.0 / self.sizey, 1)
        self.Scale(1, value, 1)
        self._sizey = value

    @property
    def sizez(self):
        return self._returnAttr('sizez', 1)

    @sizez.setter
    def sizez(self, value):
        self.Scale(1, 1, 1.0 / self.sizez)
        self.Scale(1, 1, value)
        self._sizez = value

    @property
    def sclx(self):
        return self._returnAttr('sclx', 1)

    @sclx.setter
    def sclx(self, value):
        self.sizex = value * self.sizex
        self._sclx = value

    @property
    def scly(self):
        return self._returnAttr('scly', 1)

    @scly.setter
    def scly(self, value):
        self.sizey = value * self.sizey
        self._scly = value

    @property
    def sclz(self):
        return self._returnAttr('sclz', 1)

    @sclz.setter
    def sclz(self, value):
        self.sizez = value * self.sizez
        self._sclz = value

    @property
    def iconname(self):
        if not hasattr(self, "_iconname"):
            self._iconname = str(self.obj.Name)
        return self._iconname

    @iconname.setter
    def iconname(self, value):
        self._iconname = value
        self.obj.Name = self._iconname

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value).lower()
        if hasattr(self, "_shape") and self._shape == value:
            return
        item = [x for x in library.get_items()
                if x["Name"].lower() == value]
        if not len(item):
            self._shape = "Custom"
            print "ERROR:", value, "wasnt found in library."
            return
        self._shape = value
        # check construction history and freeze
        if len([__ for __ in self.obj.ConstructionHistory]) > 1:
            app.FreezeObj(self.obj)
        item = item[0]
        self.obj.Geometry = item

        #setting transforms
        self.Translate(self.posx, self.posy, self.posz)
        self.Rotate(self.rotx, self.roty, self.rotz)
        self.Scale(self.sizex, self.sizey,
                   self.sizez)

    @property
    def size(self):
        if not hasattr(self, "_size"):
            self._size = 1
        return self._size

    @size.setter
    def size(self, value):
        self.sizex += value - self.size
        self.sizey += value - self.size
        self.sizez += value - self.size

        self._size = value

    @property
    def connect(self):
        if not hasattr(self, "_connect"):
            self._connect = None
        return self._connect

    @connect.setter
    def connect(self, obj):
        if obj:
            if self.connect:
                if not self.connect.node == obj.node:
                    try:
                        self.connect_line.Delete()
                    except:
                        pass
                    self.connect_line = app.createConnect([self.obj, obj])
            else:
                self.connect_line = app.createConnect([self.obj, obj])
        else:
            self.connect_line.Delete()
            self.connect_line = obj
        self._connect = obj

    @property
    def connect_line(self):
        if not hasattr(self, "_connect_line"):
            self._connect_line = None
        return self._connect_line

    @connect_line.setter
    def connect_line(self, obj):
        self._connect_line = obj
