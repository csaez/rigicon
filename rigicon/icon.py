from collections import OrderedDict
from wishlib.si import disp, si, siget, SIWrapper, no_inspect
from . import library

DEFAULT_DATA = {"priority": 0, "size": 1.0,
                "colorr": 1.0, "colorg": 0.882, "colorb": 0.0,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0,
                "behaviour": "srt", "shape": "Null", "connect": ""}
PROPERTY_NAME = "RigIcon_Data"
APPLYTRANSFORM_COMPOUND = "RigIcon__ApplyTransform"
CONNECT_COMPOUND = "RigIcon__ConnectionLine"

# override DEFAULT_DATA using an OrderedDict to ensure ICETrees are the last
# attribute to be processed and avoid ICE refresh isues.
DEFAULT_DATA = OrderedDict(sorted(DEFAULT_DATA.items(),
                                  key=lambda x: x[0] in ("shape", "connect")))


def is_icon(obj):
    if obj.Type == "crvlist" and obj.Properties(PROPERTY_NAME) is not None:
        return True
    return False


class Icon(SIWrapper):
    @classmethod
    def create(cls, name="rigicon", **options):
        obj = si.ActiveSceneRoot.AddNurbsCurve()
        obj.AddProperty("Display Property")
        obj.Name = name
        icon = cls(obj)
        for k, v in options.iteritems():
            if hasattr(icon, k):
                setattr(icon, k, v)
        return icon

    def __new__(cls, obj):
        if obj.Type == "crvlist":
            return SIWrapper.__new__(cls, obj)
        print "ERROR:", obj, "type isnt an icon object."

    def __init__(self, obj):
        super(Icon, self).__init__(obj, PROPERTY_NAME)
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)
        # SOFTIMAGE BUG: dispatch attributes created on SIWrapper, if they
        # are not dispatched then __setattr__ calls FAIL
        self.obj = disp(self.obj)
        self.holder = disp(self.holder)

    @property
    def iconname(self):
        if not hasattr(self, "_iconname"):
            self._iconname = self.obj.Name
        return self._iconname

    @iconname.setter
    def iconname(self, value):
        self._icon_name = value
        self.obj.Name = self._iconname

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = str(value).lower()
        if hasattr(self, "_shape") and self._shape == value:
            return
        item = [x for x in library.get_items() if x.name.lower() == value]
        if not len(item):
            print "ERROR:", value, "doesnt found on library."
            return
        self._shape = value
        si.FreezeObj(self.obj)
        self.obj.ActivePrimitive.Geometry.Set(*item[0].data)
        self.apply_transform  # ensure apply_transform exists

    @property
    def colorr(self):
        return self._colorr

    @colorr.setter
    def colorr(self, value):
        self.obj.Properties("Display").Parameters("wirecolorr").Value = value
        self._colorr = value

    @property
    def colorg(self):
        return self._colorg

    @colorg.setter
    def colorg(self, value):
        self.obj.Properties("Display").Parameters("wirecolorg").Value = value
        self._colorg = value

    @property
    def colorb(self):
        return self._colorb

    @colorb.setter
    def colorb(self, value):
        self.obj.Properties("Display").Parameters("wirecolorb").Value = value
        self._colorb = value

    @property
    @no_inspect
    def apply_transform(self):
        # find and return the ICETree
        for icetree in self.obj.ActivePrimitive.ICETrees:
            if icetree.Name == APPLYTRANSFORM_COMPOUND:
                return icetree
        # icetree doesnt found, return a new one
        return si.ApplyICEOp(APPLYTRANSFORM_COMPOUND, self.obj)

    @property
    def connect(self):
        param = siget("{0}.{1}.Reference".format(self.connect_op.FullName,
                                                 CONNECT_COMPOUND))
        return siget(param.Value)

    @connect.setter
    def connect(self, obj):
        param = siget("{0}.{1}.Reference".format(self.connect_op.FullName,
                                                 CONNECT_COMPOUND))
        try:
            param.Value = obj.FullName
        except:
            param.value = ""

    @property
    @no_inspect
    def connect_op(self):
        for icetree in self.obj.ActivePrimitive.ICETrees:
            if icetree.Name == CONNECT_COMPOUND:
                return icetree
        return si.ApplyICEOp(CONNECT_COMPOUND, self.obj)
