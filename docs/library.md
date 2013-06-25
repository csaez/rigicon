`rigicon.library` module
========================
This module helps to manage curve data into the library.

### rigicon.library.`get_items()`
Returns a `list` of `LibraryItems` on the system.

    from rigicon import library
    for item in library.get_items():
        print item.name

rigicon.library.`LibraryItem(name)`
-----------------------------------
This class represent a library item, you should pass a `str` representing the name to the constructor.

    from rigicon import library
    item = library.LibraryItem("my_item")

### LibraryItem.`name`
Gives read/write access to a `str` object representing the name of the item.

### LibraryItem.`data`
Gives read/write access to a tuple object with the curve geometry data.

The data format is the one used by Softimage, for furter details refer to [NurbsCurveList.Get2](http://download.autodesk.com/global/docs/softimage2014/en_us/sdkguide/si_om/NurbsCurveList.Get2.html).

    curve = Application.Selection(0)
    item = library.LibraryItem(curve.Name)
    item.data = curve.ActivePrimitive.Geometry.Get2()

### LibraryItem.`file`
Gives read only acces to the filepath with the data on disk.

### LibraryItem.`destroy()`
This method destroy all the dependencies of the LibraryItem, returns `True` if the operation was succesfull, otherwise it returns `False`.

    from rigicon import library
    for item in library.get_items():
        if item.name == "delete_me":
            item.destroy()
