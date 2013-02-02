import sys
import unittest

sys.path.append("/home/dionyses/projects/shelobpy/")

from core.strategy import StrategyTests


suite = unittest.TestLoader().loadTestsFromTestCase(StrategyTests)
unittest.TextTestRunner(verbosity=2).run(suite)
