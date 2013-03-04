import unittest

GUINEA_PIG = "file:///home/dionyses/projects/korlat/korlat/tests/guineapig.html"

from korlat.tests import unit
from unit import strategy, element, container, \
    windowlinks, containervisibility, elementlist, \
    unique, util


def all_unit():
    suites = [
        strategy.suite(),
        element.suite(),
        elementlist.suite(),
        container.suite(),
        windowlinks.suite(),
        containervisibility.suite(),
        unique.suite(),
        util.suite(),
    ]

    return unittest.TestSuite(suites)

