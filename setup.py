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
    url="https://www.github.com/csaez/rigicon",
    license="GNU General Public License (GPLv3)",
    install_requires=["wishlib >= 0.2.0"],
    scripts=["RigIconPlugin.py"]
)
