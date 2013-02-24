ID = "id"
"""The 'id' lookup strategy (ie: find_element_by_id())
"""
TAG = "tag"
"""The 'tag' lookup strategy (ie: find_element_by_tag_name())
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
    elif strategy == TAG:
        return "//%s" % (identifier % tuple(contents))
    elif strategy == XPATH:
        return identifier % tuple(contents)

