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

import types

from pymel import core as pm

#from .. import library
from rigicon import library

import wishlib.ma as app
reload(app)

DEFAULT_DATA = {"size": 1.0, "_shape": "Null", "_connect": None,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0,
                "sizex": 1.0, "sizey": 1.0, "sizez": 1.0}


def is_icon(obj):
    attrs = pm.listAttr(obj, ud=True)
    if obj.getShape().nodeType() == 'nurbsCurve' and \
     'metadata_namespace' in attrs:
        return True
    return False


class Icon(app.Wrapper):

    @classmethod
    def create(cls, name="rigicon", **options):
        obj = pm.circle(ch=False)[0]
        obj = pm.rename(obj, name)
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
            try:
                obj = pm.PyNode(obj)
            except:
                node = pm.circle(ch=False)[0]
                obj = pm.rename(node, obj)

        if obj.getShape().nodeType() == 'nurbsCurve':
            return app.Wrapper.__new__(cls, obj)
        print "ERROR:", obj, "type isnt an icon object."

    def __init__(self, obj):

        super(Icon, self).__init__(obj)
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

        #updating icon
        self.shape = self.shape

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

        #storing selection
        sel = pm.ls(selection=True)

        #generating curves from data
        data = item[0]
        crvs = list()
        for i in range(data["Count"]):
            start = sum(data["NbControlPoints"][:i])
            end = sum(data["NbControlPoints"][:i + 1])
            pts = zip(*data["ControlPoints"][:-1])[start:end]
            if data["Closed"][i]:
                pts.append(pts[0])
            crvs.append(pm.curve(degree=1, p=pts))

        #deleting existing curves
        for shp in self.node.getShapes():
            pm.delete(shp)

        #combining curves
        for crv in crvs:
            shp = crv.getShape()
            shp = pm.rename(shp, self.node + 'Shape')
            pm.parent(shp, self.node, r=True, s=True)
            pm.delete(crv)

        #restoring selection
        if sel:
            pm.select(sel)
        else:
            pm.select(cl=True)

    @property
    def connect(self):
        return self._connect

    @connect.setter
    def connect(self, obj):
        try:
            if isinstance(obj, pm.PyNode):
                self._connect = obj
                self.connect_line = self.createConnect(obj)
            elif isinstance(obj, types.NoneType):
                self._connect = None
                self.connect_line = None
            elif isinstance(obj, str):
                self._connect = pm.PyNode(obj)
                self.connect_line = self.createConnect(pm.PyNode(obj))
            else:
                self._connect = obj.node
                self.connect_line = self.createConnect(obj.node)
        except:
            pass

    @property
    def connect_line(self):
        return self._connect_line

    @connect_line.setter
    def connect_line(self, obj):
        if isinstance(obj, types.NoneType):
            if self._connect_line:
                pm.delete(self._connect_line)
        else:
            self._connect_line = obj

    def createConnect(self, destination):
        #storing selection
        sel = pm.ls(selection=True)

        objs = [self.node, destination]
        pts = []
        for obj in objs:
            pts.append(pm.xform(obj, translation=True, q=True))

        crv = pm.curve(degree=1, p=pts)
        crv.overrideEnabled.set(1)
        crv.overrideDisplayType.set(2)

        index = 0
        for obj in objs:
            cluster = pm.cluster(crv + '.cv[%s]' % index)[1]
            pm.parent(cluster, objs[index])
            pm.setAttr(cluster + '.visibility', 0)
            index += 1

        #restoring selection
        if sel:
            pm.select(sel)

        crv = pm.rename(crv, self.node + '_connect')
        return crv
