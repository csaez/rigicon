`rigicon.library`
===============
This module helps to manage curve data into the library.

rigicon.library.`LibraryItem`
-----------------------------
This class represent a library item 

### LibraryItem.`name`
Gives read/write access to a `str` object representing the name of the item.

### LibraryItem.`data`
Gives read/write access to a tuple object with the curve geometry data.

The data format is the one used by Softimage, for furter details refer to [`NurbsCurveList.Get2`](http://download.autodesk.com/global/docs/softimage2014/en_us/sdkguide/si_om/NurbsCurveList.Get2.html).

### LibraryItem.`file`
Gives read only acces to the on disk file with the data.

### LibraryItem.`destroy()`
This method destroy all the dependencies of the LibraryItem, returns True if the operation was succesful or false otherwise.

rigicon.library.`items`
-----------------------
Gives acces to a list of `LibraryItems` on the library, you can add remove items using standard list methods.

    import rigicon.library as lib
    for item in lib.items:
        print item.name
        print item.file