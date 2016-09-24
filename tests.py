try:
    import maya.cmds as mc
except ImportError:
    import sys
    import mock
    sys.modules["maya"] = sys.modules["maya.cmds"] = mc = mock.MagicMock()

import functools
import unittest
import logging
import rigicon


logger = logging.getLogger("rigicon")
logger.addHandler(logging.StreamHandler())


def logDebug(func):
    @functools.wraps(func)
    def decorated(*args, **kwds):
        logger.setLevel(logging.DEBUG)
        rval = None
        try:
            rval = func(*args, **kwds)
        finally:
            logger.setLevel(logging.NOTSET)
        return rval
    return decorated


class UsageCase(unittest.TestCase):
    @logDebug
    def test_create(self):
        self.assertIsNotNone(rigicon.create("foo"))


def runner():
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    runner()
