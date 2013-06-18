from wishlib.si import si, SIWrapper
from . import library

DEFAULT_DATA = {"shape": "Null",
                "connect": None,
                "priority": 0, "size": 1.0,
                "wirecolorr": 1.0, "wirecolorg": 0.882, "wirecolorb": 0.0,
                "posx": 0.0, "posy": 0.0, "posz": 0.0,
                "rotx": 0.0, "roty": 0.0, "rotz": 0.0,
                "sclx": 1.0, "scly": 1.0, "sclz": 1.0,
                "behaviour": "srt"}
PROPERTY_NAME = "RigIcon_Data"
APPLYTRANSFORM_COMPOUND = "csRigIcon__ApplyTransform"
CONNECT_COMPOUND = "csRigIcon__ConnectionLine"


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
        item = [x for x in library.get_items() if x.name.lower() == value.lower()]
        if not len(item):
            print "ERROR:", value, "doesnt found on library."
            return
        item = item[0]
        self._shape = value
        si.FreezeObj(self.obj)
        self.obj.ActivePrimitive.Geometry.Set(*item.data)

    @property
    def wirecolorr(self):
        return self._wirecolorr

    @wirecolorr.setter
    def wirecolorr(self, value):
        self.obj.Properties("Display").Parameters("wirecolorr").Value = value
        self._wirecolorr = value

    @property
    def wirecolorg(self):
        return self._wirecolorg

    @wirecolorg.setter
    def wirecolorg(self, value):
        self.obj.Properties("Display").Parameters("wirecolorg").Value = value
        self._wirecolorg = value

    @property
    def wirecolorb(self):
        return self._wirecolorb

    @wirecolorb.setter
    def wirecolorb(self, value):
        self.obj.Properties("Display").Parameters("wirecolorb").Value = value
        self._wirecolorb = value
