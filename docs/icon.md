`rigicon.icon` module
=====================
### rigicon.icon.`is_icon(obj)`
Returns `True` if the passed obj (a softimage curve) was already converted to a `Icon()` object, otherwise it returns `False`.


rigicon.icon.`Icon(obj)`
---------------------------
This class extend softimage curve functionality.
The constructor is expecting a softimage object, if the softimage object type is not `crvlist` then then instance is not created.

    from rigicon.icon import Icon
    sisel = Application.Selection
    Icon(sisel(0))

### Icon.`create(name="rigicon", **options)`:
This classmethod create a new `Icon` instance, it expect a `str` to use it as the name and a keyword parameter representing any attribute value you want to set on creation.

    from rigicon.icon import Icon
    
    # create a new icon passing some parameters
    icon = Icon.create("my_icon", shape="box", size=0.5)
    
    # the line above is a shortcut for...
    icon = Icon.create("my_icon")
    icon.shape = "box"
    icon.size = 0.5

### Icon.`iconname`
Gives read/write access to icon's name as `str`.

### Icon.`shape`
Gives read/write access to icon geometric shape as `str`, the name should correspond to the name of some item on the library.

### Icon.`connect`
The rigicon object will draw an interactive line (opengl) to this target.
Gives read/write access as a `softimage x3dobject instance`.


### Icon.`posx`/`posy`/`posz`
Gives read/write access to offset shape position coords as `float`.

### Icon.`rotx`/`roty`/`rotz`
Gives read/write access to offset shape rotation coords as `float`.

### Icon.`sclx`/`scly`/`sclz`
Gives read/write access to offset shape scale coords as `float`.

### Icon.`wirecolorr`/`wirecolorg`/`wirecolorb`
Gives read/write access to normalized color components as `int`.
