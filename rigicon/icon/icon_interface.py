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

from collections import OrderedDict

DEFAULT_DATA = {"size": 1.0, "shape": "Null", "connect": None,
                "colorr": 1.0, "colorg": 0.882, "colorb": 0.0,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0}

# override DEFAULT_DATA using an OrderedDict to ensure ICETrees are the last
# attribute to be processed and avoid ICE refresh isues.
DEFAULT_DATA = OrderedDict(
    sorted(DEFAULT_DATA.items(), key=lambda x: x[0] in ("shape", "connect")))


def is_icon(obj):
    pass


class IconInterface(object):

    @classmethod
    def create(cls, name="rigicon", **options):
        icon = cls(name)
        for k, v in options.iteritems():
            if hasattr(icon, k):
                setattr(icon, k, v)
        return icon

    @classmethod
    def new(cls, *args, **kwds):
        return cls.create(*args, **kwds)

    def __init__(self, obj):
        super(IconInterface, self).__init__()
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

    @property
    def iconname(self):
        pass

    @iconname.setter
    def iconname(self, value):
        pass

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value).lower()
        if hasattr(self, "_shape") and self._shape == value:
            return
        pass

    @property
    def color(self):
        return [int(x * 255) for x in (self.colorr, self.colorg, self.colorb)]

    @color.setter
    def color(self, rgb_list):
        for i, c in enumerate("rgb"):
            setattr(self, "color" + c, rgb_list[i] / 255.0)

    @property
    def colorr(self):
        return self._colorr

    @colorr.setter
    def colorr(self, value):
        self._colorr = value

    @property
    def colorg(self):
        return self._colorg

    @colorg.setter
    def colorg(self, value):
        self._colorg = value

    @property
    def colorb(self):
        return self._colorb

    @colorb.setter
    def colorb(self, value):
        self._colorb = value

    @property
    def apply_transform(self):
        pass

    @property
    def connect(self):
        if hasattr(self, "_connect"):
            return self._connect

    @connect.setter
    def connect(self, obj):
        if not obj:
            return
        self._connect = obj

    @property
    def connect_op(self):
        pass

    @property
    def attr_display(self):
        pass
