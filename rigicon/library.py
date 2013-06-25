import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config")
EXCEPTION = ("__init__.py")


def get_items():
    items = list()
    for filename in os.listdir(CONFIG_PATH):
        f = os.path.join(CONFIG_PATH, filename)
        if os.path.isfile(f) and filename not in EXCEPTION:
            items.append(LibraryItem(filename.replace(".py", "")))
    return items


class LibraryItem(object):
    def __init__(self, name):
        self._name = name
        if os.path.isfile(self.file):
            self.data = self._fromfile()

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._data = list()
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._tofile(self.data)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        os.rename(self.file, self.file.replace(self._name, name))
        self._name = name

    @property
    def file(self):
        if not hasattr(self, "_file"):
            self._file = os.path.join(
                CONFIG_PATH, "{}.py".format(self.name))
        return self._file

    def destroy(self):
        try:
            os.remove(self.file)
            return True
        except:
            print "ERROR: file doesnt found or in use."
            return False

    def _fromfile(self):
        with open(self.file) as f:
            return eval(f.read())

    def _tofile(self, data):
        with open(self.file, "w") as f:
            f.write(str(data))
