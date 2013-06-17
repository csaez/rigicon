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

### Icon.`create(name="rig_icon")`:
This classmethod create a new `Icon` instance, it expect a `str` to use it as the name.

### Icon.`set_position(x, y, z)`:
Set shape offset position where `x`, `y` and `z` are `float` representing the coordinates.

### Icon.`set_rotation(x, y, z)`:
Set shape offset scale where `x`, `y` and `z` are `float` representing the rotation components (degrees).

### Icon.`set_scale(x, y, z)`:
Set shape offset shape scale where `x`, `y` and `z` are `float` representing the scale components.

### Icon.`set_wirecolor(r, g, b)`:
Set wireframe color where `r`, `g` and `b` are `int` representing the color components.

#### Attributes:
* `icon_name`:
Gives read-only access to the icon's name as `str`.

* `posx`/`posy`/`posz`:
Gives read/write access to offset shape position coords as `float`.

* `rotx`/`roty`/`rotz`:
Gives read/write access to offset shape rotation coords as `float`.

* `sclx`/`scly`/`sclz`:
Gives read/write access to offset shape scale coords as `float`.

* `wirecolorr`/`wirecolorg`/`wirecolorb`:
Gives read/write access to color components as `int`.
