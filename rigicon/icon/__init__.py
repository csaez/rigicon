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

from wishlib import inside_softimage, inside_maya

if inside_softimage():
    from .icon_softimage import Icon, is_icon
elif inside_maya():
    import icon_maya
    reload(icon_maya)
    from icon_maya import Icon, is_icon
else:
    from .icon_interface import IconInterface, is_icon

    class Icon(IconInterface):
        pass
