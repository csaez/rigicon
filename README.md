# RigIcon

A _very_ simple icon library for Autodesk Maya providing a convenient way to
create, edit and manage animation controls for your rigs.


## Installation

Copy `rigicon.py` to a directory in your python path within maya (i.e.
`~/maya/scripts/`) or install it as a python package through its `setup.py`
script.

    python setup.py install


## Usage

```python
import maya.cmds as mc
import rigicon


# Create a std maya transform node to be used as your animation control
xfo = mc.createNode("transform", name="foo")

# Attach an icon
rigicon.set(xfo, icon="square")  # square being defined on rigicon library



# List icons on the library
print(rigicon.library.list())

# Remove an item from the library (this does not affect existing anim controls)
rigicon.library.remove("square")

# Add the selected shape(s) to the library
rigicon.library.add("fancy", mc.ls(sl=True))



# Apply this new icon to the existing transform node + offsets (shape node only)
rigicon.set(xfo, icon="fancy",
            translate=[0.3, 20.5, 0.0],
            rotate=[33.3, 0.0, 45.0],
            scale=[2.0, 1.0, 1.0])

# ... or apply local transforms as icon offsets instead of typing it down
rigicon.setNeutral(xfo)



# You can also do all of the above in a single and convenient call
xfo = rigicon.create("foo", icon="fancy",
                     translate=[0.3, 20.5, 0.0],
                     rotate=[33.3, 0.0, 45.0],
                     scale=[2.0, 1.0, 1.0])
```

For technical details please refer to the [documentation](http://cesarsaez.me/rigicon/).




## Contributing

- [Check for open issues](https://github.com/csaez/rigicon/issues) or open a
  fresh issue to start a discussion around a feature idea or a bug.
- Fork the [rigicon repository on Github](https://github.com/csaez/rigicon) to
  start making your changes (make sure to isolate your changes in a local
  branch).
- Write a test showing that the bug was fixed or that the feature works as
  expected.
- Send a pull request and bug me until it gets merged :)
