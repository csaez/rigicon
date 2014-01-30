# This file is part of rigicon
# Copyright (C) 2014  Cesar Saez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from wishlib.si import si, siget, log, C, show_qt


def XSILoadPlugin(in_reg):
    in_reg.Name = "RigIcon Plugin"
    in_reg.Author = "csaez"
    in_reg.Major = 1.0
    in_reg.Minor = 0.0
    in_reg.UserData = ""
    in_reg.RegisterCommand("RigIcon Library", "RigIconLibrary")
    in_reg.RegisterCommand("RigIcon Editor", "RigIconEditor")
    in_reg.RegisterCommand("RigIcon", "RigIcon")
    in_reg.RegisterFilter("RigIcon", C.siFilter3DObject)
    return True


def XSIUnloadPlugin(in_reg):
    log("{} has been unloaded".format(in_reg.Name), C.siVerbose)
    return True


def RigIconLibrary_Execute():
    log("RigIconLibrary_Execute called", C.siVerbose)
    from rigicon.layout.library_gui import RigIconLibrary
    show_qt(RigIconLibrary)
    return True


def RigIconEditor_Execute():
    log("RigIconEditor_Execute called", C.siVerbose)
    from rigicon.layout.editor_gui import RigIconEditor
    show_qt(RigIconEditor)
    return True


def RigIcon_Execute():
    log("RigIcon_Execute called", C.siVerbose)
    from rigicon.icon import Icon
    icon = Icon.create()
    if siget("preferences.modeling.selectgeneratedobj"):
        si.SelectObj(icon.obj)
    return True


def RigIcon_Match(in_ctxt):
    log("RigIconFilter_Match called", C.siVerbose)
    obj = in_ctxt.GetAttribute("Input")
    from rigicon.icon import is_icon
    return is_icon(obj)
