import sys
import unittest

sys.path.append("/home/dionyses/projects/korlat/korlat/")

from unit import strategy, element, container, \
    windowlinks, containervisibility


suites = [
    strategy.suite(),
    element.suite(),
    container.suite(),
    windowlinks.suite(),
    containervisibility.suite(),
]

all_unit_tests = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(all_unit_tests)
