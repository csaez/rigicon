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

from .. import library

import wishlib.ma as app
reload(app)

DEFAULT_DATA = {"size": 1.0, "shape": "Null", "connect": None,
                "colorr": 1.0, "colorg": 0.882, "colorb": 0.0,
                "_posx": 0.0, "_posy": 0.0, "_posz": 0.0,
                "_rotx": 0.0, "_roty": 0.0, "_rotz": 0.0,
                "_sclx": 1.0, "_scly": 1.0, "_sclz": 1.0,
                "_sizex": 1.0, "_sizey": 1.0, "_sizez": 1.0,
                "_size": 1.0}


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

    def __new__(cls, obj='rigicon'):

        if isinstance(obj, str):
            try:
                obj = pm.PyNode(obj)
            except:
                node = pm.circle(ch=False)[0]
                obj = pm.rename(node, obj)

        if obj.getShape().nodeType() == 'nurbsCurve':
            return app.Wrapper.__new__(cls, obj)
        print "ERROR:", obj, "type isnt an icon object."

    def __init__(self, obj='rigicon'):

        #adding exceptions for class properties
        exceptions = ['iconname', 'shape', 'connect',
                      'sizex', 'sizey', 'sizez',
                      'posx', 'posy', 'posz',
                      'rotx', 'roty', 'rotz',
                      'connect_line', 'size']

        for e in exceptions:
            self.EXCEPTIONS.append(e)

        super(Icon, self).__init__(obj)
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

        #updating icon
        self.shape = self.shape

    def scale(self, x, y, z):
        with pm.UndoChunk():
            bb = pm.xform(self.node, q=True, bb=True, ws=True)
            centerX = (bb[0] + bb[3]) / 2.0
            centerY = (bb[1] + bb[4]) / 2.0
            centerZ = (bb[2] + bb[5]) / 2.0

            for shp in self.node.getShapes():
                pm.scale(pm.PyNode(shp + '.cv[*]'), [x, y, z],
                         pivot=[centerX, centerY, centerZ])

    def rotate(self, x, y, z):
        with pm.UndoChunk():
            bb = pm.xform(self.node, q=True, bb=True, ws=True)
            centerX = (bb[0] + bb[3]) / 2.0
            centerY = (bb[1] + bb[4]) / 2.0
            centerZ = (bb[2] + bb[5]) / 2.0

            for shp in self.node.getShapes():
                pm.rotate(pm.PyNode(shp + '.cv[*]'), [x, y, z],
                         pivot=[centerX, centerY, centerZ])

    def translate(self, x, y, z):
        with pm.UndoChunk():
            for shp in self.node.getShapes():
                pm.move(pm.PyNode(shp + '.cv[*]'), [x, y, z],
                        r=True)

    @property
    def posx(self):
        return self._posx

    @posx.setter
    def posx(self, value):
        self.translate((self.posx * -1), 0, 0)
        self.translate(value, 0, 0)
        self._posx = float(value)

    @property
    def posy(self):
        return self._posy

    @posy.setter
    def posy(self, value):
        self.translate(0, (self.posy * -1), 0)
        self.translate(0, value, 0)
        self._posy = float(value)

    @property
    def posz(self):
        return self._posz

    @posz.setter
    def posz(self, value):
        self.translate(0, 0, (self.posz * -1))
        self.translate(0, 0, value)
        self._posz = float(value)

    @property
    def rotx(self):
        return self._rotx

    @rotx.setter
    def rotx(self, value):
        self.rotate((self.rotx * -1), 0, 0)
        self.rotate(value, 0, 0)
        self._rotx = float(value)

    @property
    def roty(self):
        return self._roty

    @roty.setter
    def roty(self, value):
        self.rotate(0, (self.roty * -1), 0)
        self.rotate(0, value, 0)
        self._roty = float(value)

    @property
    def rotz(self):
        return self._rotz

    @rotz.setter
    def rotz(self, value):
        self.rotate(0, 0, (self.rotz * -1))
        self.rotate(0, 0, value)
        self._rotz = float(value)

    @property
    def sclx(self):
        return self._sclx

    @sclx.setter
    def sclx(self, value):
        self.sizex = value * self.sizex
        self._sclx = float(value)

    @property
    def scly(self):
        return self._scly

    @scly.setter
    def scly(self, value):
        self.sizey = value * self.sizey
        self._scly = float(value)

    @property
    def sclz(self):
        return self._sclz

    @sclz.setter
    def sclz(self, value):
        self.sizez = value * self.sizez
        self._sclz = float(value)

    @property
    def sizex(self):
        return self._sizex

    @sizex.setter
    def sizex(self, value):
        self.scale(1.0 / self.sizex, 1, 1)
        self.scale(value, 1, 1)
        self._sizex = float(value)

    @property
    def sizey(self):
        return self._sizey

    @sizey.setter
    def sizey(self, value):
        self.scale(1, 1.0 / self.sizey, 1)
        self.scale(1, value, 1)
        self._sizey = float(value)

    @property
    def sizez(self):
        return self._sizez

    @sizez.setter
    def sizez(self, value):
        self.scale(1, 1, 1.0 / self.sizez)
        self.scale(1, 1, value)
        self._sizez = float(value)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self.sizex += value - self.size
        self.sizey += value - self.size
        self.sizez += value - self.size

        self._size = float(value)

    @property
    def iconname(self):
        return str(self.node)

    @iconname.setter
    def iconname(self, value):
        self.node = pm.rename(self.node, value)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        with pm.UndoChunk():
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

        with pm.UndoChunk():

            #storing selection
            sel = pm.ls(selection=True)

            objs = [self.node, destination]
            pts = []
            for obj in objs:
                pts.append(pm.xform(obj, translation=True, q=True))

            crv = pm.curve(degree=1, p=pts)
            crv.overrideEnabled.set(1)
            crv.overrideDisplayType.set(2)
            crv.inheritsTransform.set(0)
            pm.parent(crv, self.node)

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
