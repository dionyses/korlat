from mock import Mock
import unittest

from korlat.abstraction.element import Element
from korlat.core.strategy import ID
from korlat.core.webapp import WebApp
from korlat.common.objects import Checkbox
from korlat.common.util import canonical_class


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_canonical_class_name(self):
        w = Mock()
        w.__class__ = WebApp

        e = Element(w, ID, "")
        self.assertEqual(canonical_class(e), "object.Element")

        c = Checkbox(w, ID, "")
        self.assertEqual(canonical_class(c), "object.Element.CheckableElement.AestheticElement.Checkbox")

        s = ""
        self.assertEqual(canonical_class(s), "object.basestring.str")


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

