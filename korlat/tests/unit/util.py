from mock import Mock
import unittest

from korlat.abstraction.element import Element
from korlat.core.strategy import ID
from korlat.core.webapp import WebApp
from korlat.common.objects import Checkbox
from korlat.common.util import canonical


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_canonical_name(self):
        w = Mock()
        w.__class__ = WebApp

        e = Element(w, ID, "")
        self.assertEqual(canonical(e), "object.Element")

        c = Checkbox(w, ID, "")
        self.assertEqual(canonical(c), "object.Element.CheckableElement.AestheticElement.Checkbox")

        s = ""
        self.assertEqual(canonical(s), "object.basestring.str")


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)

