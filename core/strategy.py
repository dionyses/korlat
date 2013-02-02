import unittest

ID = "id"
"""The 'id' lookup strategy (ie: find_element_by_id())
"""
XPATH = "xpath"
"""The 'xpath' lookup strategy (ie: find_element_by_xpath())
"""

def xpath_of(strategy, identifier, contents=[]):
    """Get the xpath compatable lookup of the strategy

    Converts the specified strategy, identifier, and contents into an xpath expression

    :param strategy: the lookup strategy which applies to the **identifier**
    :type strategy: :py:const:`strategy`
    :param identifier: the value to search for
    :type identifier: str
    :param contents: if applicable, the contents used to fill **identifier**
    :type contents: list
    """
    if strategy == ID:
        return "//*[@id='%s']" % (identifier % tuple(contents))
    elif strategy == XPATH:
        return identifier % tuple(contents)


class StrategyTests(unittest.TestCase):
    def setUp(self):
        pass

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

