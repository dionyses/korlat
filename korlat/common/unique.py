from datetime import datetime
import threading

_lock = threading.Lock()
_previous = set([])


def identifier(prefix=""):
    """Get the next unique string identifier

    >>> identifier()
    130224-115230-5495
    >>> identifier()
    130224-115230-2054
    >>> identifier()
    130224-115231-6135
    >>> identifier("special")
    special-130224-115231-9374

    :param prefix: an optional argument which will be used to prefix the next unique string
    :returns: a unique string
    """
    global _previous
    # ensure no two threads request a unique identifier at the exact same time
    _lock.acquire()
    out = _identifier(prefix)

    # TODO: I can't figure out why the locking isn't always providing
    # a unique string -> unit test failure
    # for now, I'm just implementing this with a non-scaling memory approach :(
    # guarantee uniqueness by checking previous identifiers value :(
    while out in _previous:
        out = _identifier(prefix)

    _previous.add(out)
    _lock.release()
    return out


def _identifier(prefix=""):
    now = datetime.now()
    out = str(prefix) if len(str(prefix)) == 0 else str(prefix) + "-"
    # grab the first 4 digits of the microsecond because its length can vary
    # and we want a constant identifier size
    out += "%s-%s" % (now.strftime("%y%m%d-%H%M%S"), str(now.microsecond)[:4])
    return out


def fqdn():
    """Get the next unique fully qualified domain name (fqdn)

    >>> fqdn()
    gjpq.gyrm.bde
    >>> fqdn()
    gjpq.gyrm.jkm

    :returns: a unique fully qualified domain name
    """
    out = []
    chunks = identifier().split("-")

    # _i_to_astr(702) yields "aaa", so anything less than
    # 702 will not produce a long enough string for the top
    # level domain
    while int(chunks[2]) < 702:
        chunks = identifier().split("-")

    for i in identifier().split("-"):
        out += [_i_to_astr(int(i))]

    return ".".join(out)


def email():
    """Get the next unique email

    >>> email()
    gjpqgzpjlnu_gjpq@gzpj.lnw
    >>> email()
    gjpqgzpkdgj_gjpq@gzpk.dgl

    :returns: a unique email
    """
    return "%s_%s" % (fqdn().replace(".", ""), fqdn().replace(".", "@", 1))


def _i_to_astr(i):
    assert i >= 0

    if i >= 26:
        return _i_to_astr((i / 26) - 1) + _i_to_astr(i % 26)
    else:
        return str(unichr(i + ord('a')))

