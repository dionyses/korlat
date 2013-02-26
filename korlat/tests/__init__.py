import unittest

GUINEA_PIG = "file:///home/dionyses/projects/korlat/korlat/tests/guineapig.html"

import unit
from unit import strategy, element, container, \
    windowlinks, containervisibility, elementlist, \
    unique


def all_unit():
    suites = [
        strategy.suite(),
        element.suite(),
        elementlist.suite(),
        container.suite(),
        windowlinks.suite(),
        containervisibility.suite(),
        unique.suite(),
    ]

    all_unit_tests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(all_unit_tests)

