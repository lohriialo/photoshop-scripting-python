# There are also propputref tests in test_sapi.py!
import unittest
from comtypes.client import CreateObject
from comtypes.automation import VARIANT

class Test(unittest.TestCase):
    def test(self, dynamic=False):
        d = CreateObject("Scripting.Dictionary", dynamic=dynamic)
        s = CreateObject("TestComServerLib.TestComServer", dynamic=dynamic)
        s.name = "the value"

        # This calls propputref, since we assign an Object
        d.Item["object"] = s
        # This calls propput, since we assing a Value
        d.Item["value"] = s.name

        self.failUnlessEqual(d.Item["object"], s)
        self.failUnlessEqual(d.Item["object"].name, "the value")
        self.failUnlessEqual(d.Item["value"], "the value")

        # Changing the default property of the object
        s.name = "foo bar"
        self.failUnlessEqual(d.Item["object"], s)
        self.failUnlessEqual(d.Item["object"].name, "foo bar")
        self.failUnlessEqual(d.Item["value"], "the value")

        # This also calls propputref since we assign an Object
        d.Item["var"] = VARIANT(s)
        self.failUnlessEqual(d.Item["var"], s)

    def test_dispatch(self):
        return self.test(dynamic=True)

if __name__ == "__main__":
    unittest.main()
