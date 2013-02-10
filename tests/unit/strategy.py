import unittest

from core.strategy import xpath_of, ID, XPATH


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_xpath(self):
        self.assertEqual("//*[@id='element_id']", xpath_of(XPATH, "//*[@id='element_id']"))

    def test_id(self):
        self.assertEqual("//*[@id='element_id']", xpath_of(ID, "element_id", []))
        self.assertEqual("//*[@id='element_x_id']", xpath_of(ID, "element_%s_id", ["x"]))
        self.assertEqual("//*[@id='element_1_id']", xpath_of(ID, "element_%d_id", [1]))

        # TypeError: not all arguments converted during string formatting
        self.assertRaisesRegexp(TypeError,
                                "not all arguments converted during string formatting",
                                xpath_of, ID, "element_id", ["asdf"])

        # TypeError: not enough arguments for format string
        self.assertRaisesRegexp(TypeError,
                                "not enough arguments for format string",
                                xpath_of, ID, "element_%s_id", [])

        # TypeError: %d format: a number is required, not str
        self.assertRaisesRegexp(TypeError,
                                "%d format: a number is required, not str",
                                xpath_of, ID, "element_%d_id", ["x"])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
