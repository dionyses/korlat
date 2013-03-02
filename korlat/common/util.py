def canonical(obj):
    """Get the canonical name of the object

    >>> s = "stringy"
    >>> canonical(s)
    object.basestring.str
    >>> c = Checkbox(my_web_app, ID, "yadda")
    >>> canonical(c)
    object.Element.CheckableElement.AestheticElement.Checkbox

    :param obj: the instance to retrieve the canonical name from
    :type obj: object
    :returns: a dot (.) delimited string which absolutely identifies the inheritance chain of the specified object
    """
    if obj.__class__ != object.__class__:
        return canonical(obj.__class__)
    elif obj.__base__ is not None:
        return "%s.%s" % (canonical(obj.__base__), obj.__name__)
    else:
        return obj.__name__

