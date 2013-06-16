from wishlib.si import si, SIWrapper

DEFAULT_DATA = {"icon": "Null", "connect": None,
                "priority": 0, "size": 1.0,
                "_wirecolorr": 1.0, "_wirecolorg": 0.882, "_wirecolorb": 0.0,
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
    def create(cls, name="rig_icon"):
        obj = si.ActiveSceneRoot.AddNurbsCurve()
        obj.AddProperty("Display Property")
        obj.Name = name
        return cls(obj)

    def __new__(cls, obj):
        if obj.Type == "crvlist":
            return SIWrapper.__new__(cls, obj)
        print "ERROR:", obj, "type isnt an icon object."

    def __init__(self, obj):
        super(Icon, self).__init__(obj, PROPERTY_NAME)
        self.wirecolorr = property(lambda: self._get_color("wirecolorr"),
                                   lambda x: self._set_color("wirecolorr", x))
        self.wirecolorg = property(lambda: self._get_color("wirecolorg"),
                                   lambda x: self._set_color("wirecolorg", x))
        self.wirecolorb = property(lambda: self._get_color("wirecolorb"),
                                   lambda x: self._set_color("wirecolorb", x))
        for k, v in DEFAULT_DATA.iteritems():
            if not hasattr(self, k):
                setattr(self, k, v)

    @property
    def icon_name(self):
        if not hasattr(self, "_icon_name"):
            self._icon_name = self.obj.Name
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value):
        self._icon_name = value
        self.obj.Name = self._icon_name

    def set_position(self, x, y, z):
        self.posx, self.posy, self.posz = x, y, z

    def set_rotation(self, x, y, z):
        self.rotx, self.roty, self.rotz = x, y, z

    def set_scale(self, x, y, z):
        self.sclx, self.scly, self.sclz = x, y, z

    def set_wirecolor(self, r, g, b):
        self.wirecolorr, self.wirecolorg, self.wirecolorb = r, g, b

    def _get_color(self, key):
        setattr(self, "_{}".format(key),
                self.obj.Properties("Display").Parameters(key).Value)
        return getattr(self, "_{}".format(key))

    def _set_color(self, key, value):
        setattr("_{}".format(key), value)
        self.obj.Properties("Display").Parameters(key).Value = value
