def canonical_class(obj):
    """Get the canonical class name of the object

    >>> s = "stringy"
    >>> canonical_class(s)
    object.basestring.str
    >>> c = Checkbox(my_web_app, ID, "yadda")
    >>> canonical_class(c)
    object.Element.CheckableElement.AestheticElement.Checkbox

    :param obj: the instance to retrieve the canonical class name from
    :type obj: object
    :returns: a dot (.) delimited string which absolutely identifies the inheritance chain of the specified object
    """
    if obj.__class__ != object.__class__:
        return canonical_class(obj.__class__)
    elif obj.__base__ is not None:
        return "%s.%s" % (canonical_class(obj.__base__), obj.__name__)
    else:
        return obj.__name__

