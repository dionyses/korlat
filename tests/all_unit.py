import sys
import unittest

sys.path.append("/home/dionyses/projects/shelobpy/")

from unit import strategy, element, container


suites = [
    strategy.suite(),
    element.suite(),
    container.suite(),
]

all_unit_tests = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(all_unit_tests)
