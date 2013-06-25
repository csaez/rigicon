from wishlib.si import log, C, show_qt


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
    from rigicon.layout.library_gui import RigIconLibrary
    show_qt(RigIconLibrary)
    return True


def RigIconEditor_Execute():
    log("csRigIconEditor_Execute called", C.siVerbose)
    from rigicon.layout.editor_gui import RigIconEditor
    show_qt(RigIconEditor)
    return True


def RigIcon_Execute():
    log("csRigIconLibrary_Execute called", C.siVerbose)
    from rigicon.icon import Icon
    Icon.create()
    return True


def RigIcon_Match(in_ctxt):
    log("csRigIconFilter_Match called", C.siVerbose)
    obj = in_ctxt.GetAttribute("Input")
    from rigicon.icon import is_icon
    return is_icon(obj)
