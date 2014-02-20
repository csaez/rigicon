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

import os
import shutil

from wishlib.utils import JSONDict
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
USER_PATH = os.path.join(os.path.expanduser("~"), "rigicon")
if not os.path.exists(USER_PATH):
    os.makedirs(USER_PATH)


def get_items():
    # first run
    if not len(os.listdir(USER_PATH)):
        # copy shapes from data
        for filename in os.listdir(DATA_PATH):
            f = os.path.join(DATA_PATH, filename)
            if os.path.isfile(f) and f.endswith(".json"):
                shutil.copy(f, USER_PATH)
    # init from user
    items = list()
    for filename in os.listdir(USER_PATH):
        f = os.path.join(DATA_PATH, filename)
        if os.path.isfile(f) and f.endswith(".json"):
            items.append(JSONDict(f))
    return items


def get_item(name):
    for x in get_items():
        if x["Name"] == name:
            return x


def rename_item(item, new_name):
    fp = item.fp
    item.fp = item.fp.replace(item["Name"], new_name)
    item["Name"] = new_name
    os.remove(fp)


def remove_item(item_name):
    for item in get_items():
        if item["Name"] == item_name:
            fp = item.fp
            del item
            os.remove(fp)


def add_item(name, curve_data):
    fp = os.path.join(USER_PATH, "{0}.json".format(name))
    item = JSONDict(fp)
    item["Name"] = name
    for i, key in enumerate(("Count", "ControlPoints", "NbControlPoints",
                             "Knots", "NbKnots", "Closed", "Degree",
                             "Parameterization")):
        item[key] = curve_data[i]
    return item
