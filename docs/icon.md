`rigicon.icon`
==============
### rigicon.icon.`is_icon(obj)`
Returns `True` if the passed obj (a softimage curve) was already converted to a `Icon()` object, otherwise it returns `False`.


rigicon.library.`Icon(obj)`
---------------------------
This class extend softimage curve functionality.
The constructor is expecting a softimage object, if the softimage object type is not `crvlist` then then instance is not created.

    from rigicon.icon import Icon
    sisel = Application.Selection
    Icon(sisel(0))

### Methods
* Icon.`create(name="rig_icon")`:

This classmethod create a new `Icon` instance, it expect a `str` to use it as the name.

* Icon.`set_position(x, y, z)`:

Set shape offset position where `x`, `y` and `z` are `float` representing the coordinates.

* Icon.`set_rotation(x, y, z)`:

Set shape offset scale where `x`, `y` and `z` are `float` representing the rotation components (degrees).

* Icon.`set_scale(x, y, z)`:

Set shape offset shape scale where `x`, `y` and `z` are `float` representing the scale components.

* Icon.`set_wirecolor(r, g, b)`:

Set wireframe color where `r`, `g` and `b` are `int` representing the color components.

### Attributes
* Icon.`icon_name`:
Gives read access to the icon's name (`str`).

* Icon.`posx`:

Gives read/write access to offset shape position `X` as `float`.

* Icon.`posy`:

Gives read/write access to offset shape position `Y` as `float`.

* Icon.`posz`:

Gives read/write access to offset shape position `Z` as `float`.

* Icon.`rotx`:

Gives read/write access to offset shape rotation `X` as `float`.

* Icon.`roty`:

Gives read/write access to offset shape rotation `Y` as `float`.

* Icon.`rotz`:

Gives read/write access to offset shape rotation `Z` as `float`.

* Icon.`sclx`:

Gives read/write access to offset shape scale `X` as `float`.

* Icon.`scly`:

Gives read/write access to offset shape scale `Y` as `float`.

* Icon.`sclz`:

Gives read/write access to offset shape scale `Z` as `float`.

* Icon.`wirecolorr`:

Gives read/write access to `red` component of the wireframe color as `int`.

* Icon.`wirecolorg`:

Gives read/write access to `green` component of the wireframe color as `int`.

* Icon.`wirecolorb`:

Gives read/write access to `blue` component of the wireframe color as `int`.
