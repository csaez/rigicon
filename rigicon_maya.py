# This file is part of rigicon.
# Copyright (C) 2014 Cesar Saez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from maya import OpenMayaMPx
from wishlib.ma import show_qt


# Commands
class rigIconLibrary(OpenMayaMPx.MPxCommand):

    def __init__(self):
        super(rigIconLibrary, self).__init__()

    # Invoked when the command is run.
    def doIt(self, argList):
        from rigicon.layout.library_gui import RigIconLibrary
        show_qt(RigIconLibrary)


class rigIconEditor(OpenMayaMPx.MPxCommand):

    def __init__(self):
        super(rigIconEditor, self).__init__()

    # Invoked when the command is run.
    def doIt(self, argList):
        from rigicon.layout.editor_gui import RigIconEditor
        show_qt(RigIconEditor)


class rigIcon(OpenMayaMPx.MPxCommand):

    def __init__(self):
        super(rigIcon, self).__init__()

    # Invoked when the command is run.
    def doIt(self, argList):
        from rigicon.icon import Icon
        Icon.new()

plugin_cmds = {"rigIconLibrary": rigIconLibrary,
               "rigIconEditor": rigIconEditor,
               "rigIcon": rigIcon}


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    for cmd_name, cmd_class in plugin_cmds.iteritems():
        try:
            mplugin.registerCommand(
                cmd_name, lambda: OpenMayaMPx.asMPxPtr(cmd_class()))
        except:
            sys.stderr.write("Failed to register command: %s\n" % cmd_name)
            raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    for cmd_name in plugin_cmds.keys():
        try:
            mplugin.deregisterCommand(cmd_name)
        except:
            sys.stderr.write(
                "Failed to unregister command: %s\n" % cmd_name)
