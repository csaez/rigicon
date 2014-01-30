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

from setuptools import setup, find_packages

setup(
    name="rigicon",
    version="0.1.0",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={"rigicon.layout": ["ui/*.ui"],
                  "rigicon": ["data/compounds/*.xsicompound"]},
    author="Cesar Saez",
    author_email="cesarte@gmail.com",
    description="A simple icon library for Softimage",
    url="http://www.github.com/csaez/rigicon",
    license="GNU General Public License (GPLv3)",
    install_requires=["wishlib >= 0.2.0"]
)
