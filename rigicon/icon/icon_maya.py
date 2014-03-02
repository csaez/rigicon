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

DEFAULT_DATA = {"_size": 1.0, "_shape": "Null", "connect": None,
                "colorr": 1.0, "colorg": 0.882, "colorb": 0.0,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0}
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
        if isinstance(obj, str):
            obj = app.Object(obj)

        super(Icon, self).__init__(obj, DATA_LINK)
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

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

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if hasattr(self, "_size") and self._size == value:
            return

        self.Scale((1.0 / self.size), self.obj.node + '.cv[*]')
        self.Scale(value, self.obj.node + '.cv[*]')

        self._size = value
