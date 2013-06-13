from wishlib.si import sianchor, log, C


def XSILoadPlugin(in_reg):
    in_reg.Name = "RigIconPlugin"
    in_reg.Author = "csaez"
    in_reg.Major = 1.0
    in_reg.Minor = 0.0
    in_reg.UserData = ""
    in_reg.RegisterCommand("RigIconLibrary", "RigIconLibrary")
    in_reg.RegisterCommand("RigIconEditor", "RigIconEditor")
    in_reg.RegisterCommand("RigIcon", "RigIcon")
    in_reg.RegisterFilter("RigIcon", C.siFilter3DObject)
    return True


def XSIUnloadPlugin(in_reg):
    log("{} has been unloaded".format(in_reg.Name), C.siVerbose)
    return True


def RigIconLibrary_Execute():
    log("csRigIconLibrary_Execute called", C.siVerbose)
    import rigicon.layout.library_gui as library
    reload(library)
    oDialog = library.GUI(sianchor())
    oDialog.show()
    return True


def RigIconEditor_Execute():
    log("csRigIconEditor_Execute called", C.siVerbose)
    import rigicon.layout.editor_gui as editor
    reload(editor)
    oDialog = editor.GUI(sianchor())
    oDialog.show()
    return True


def RigIcon_Execute():
    log("csRigIconLibrary_Execute called", C.siVerbose)
    import rigicon.icon as icon
    reload(icon)
    icon.Icon.create()
    return True


def RigIcon_Match(in_ctxt):
    log("csRigIconFilter_Match called", C.siVerbose)
    obj = in_ctxt.GetAttribute("Input")
    if obj.Type == "crvlist" and obj.Properties("RigIcon_Data") is not None:
        return True
    return False
