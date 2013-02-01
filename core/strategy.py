ID = "id"
XPATH = "xpath"

def xpath(strategy, identifier, contents=[]):
    if strategy == ID:
        return "//*[@id='%s']" % (identifier % tuple(contents))
    elif strategy == XPATH:
        return identifier % tuple(contents)

