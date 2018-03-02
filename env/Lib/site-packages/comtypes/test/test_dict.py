"""Use Scripting.Dictionary to test the lazybind module."""

import unittest
from comtypes import COMError
from comtypes.client import CreateObject
from comtypes.client.lazybind import Dispatch
from comtypes.automation import VARIANT

class Test(unittest.TestCase):
    def test_dict(self):
        d = CreateObject("Scripting.Dictionary", dynamic=True)
        self.failUnlessEqual(type(d), Dispatch)

        # Count is a normal propget, no propput
        self.failUnlessEqual(d.Count, 0)
        self.assertRaises(AttributeError, lambda: setattr(d, "Count", -1))

        # HashVal is a 'named' propget, no propput
        ##d.HashVal

        # Add(Key, Item) -> None
        self.failUnlessEqual(d.Add("one", 1), None)
        self.failUnlessEqual(d.Count, 1)

        # RemoveAll() -> None
        self.failUnlessEqual(d.RemoveAll(), None)
        self.failUnlessEqual(d.Count, 0)

        # CompareMode: propget, propput
        # (Can only be set when dict is empty!)
        self.failUnlessEqual(d.CompareMode, 0)
        d.CompareMode = 1
        self.failUnlessEqual(d.CompareMode, 1)
        d.CompareMode = 0

        # Exists(key) -> bool
        self.failUnlessEqual(d.Exists(42), False)
        d.Add(42, "foo")
        self.failUnlessEqual(d.Exists(42), True)

        # Keys() -> array
        # Items() -> array
        self.failUnlessEqual(d.Keys(), (42,))
        self.failUnlessEqual(d.Items(), ("foo",))
        d.Remove(42)
        self.failUnlessEqual(d.Exists(42), False)
        self.failUnlessEqual(d.Keys(), ())
        self.failUnlessEqual(d.Items(), ())

        # Item[key] : propget
        d.Add(42, "foo")
        self.failUnlessEqual(d.Item[42], "foo")

        d.Add("spam", "bar")
        self.failUnlessEqual(d.Item["spam"], "bar")

        # Item[key] = value: propput, propputref
        d.Item["key"] = "value"
        self.failUnlessEqual(d.Item["key"], "value")
        d.Item[42] = 73, 48
        self.failUnlessEqual(d.Item[42], (73, 48))

        ################################################################
        # part 2, testing propput and propputref

        s = CreateObject("Scripting.Dictionary", dynamic=True)
        s.CompareMode = 42

        # This calls propputref, since we assign an Object
        d.Item["object"] = s
        # This calls propput, since we assing a Value
        d.Item["value"] = s.CompareMode

        a = d.Item["object"]
 
        self.failUnlessEqual(d.Item["object"], s)
        self.failUnlessEqual(d.Item["object"].CompareMode, 42)
        self.failUnlessEqual(d.Item["value"], 42)

        # Changing a property of the object
        s.CompareMode = 5
        self.failUnlessEqual(d.Item["object"], s)
        self.failUnlessEqual(d.Item["object"].CompareMode, 5)
        self.failUnlessEqual(d.Item["value"], 42)

        # This also calls propputref since we assign an Object
        d.Item["var"] = VARIANT(s)
        self.failUnlessEqual(d.Item["var"], s)

        # iter(d)
        keys = [x for x in d]
        self.failUnlessEqual(d.Keys(),
                             tuple([x for x in d]))

        # d[key] = value
        # d[key] -> value
        d["blah"] = "blarg"
        self.failUnlessEqual(d["blah"], "blarg")
        # d(key) -> value
        self.failUnlessEqual(d("blah"), "blarg")

if __name__ == "__main__":
    unittest.main()
