


HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"


class AppUrl(object):
    def __init__(self, host, port=None, relative=None):
        super(AppUrl, self).__init__()

        if relative is not None:
            assert relative[0] == "/"

        self.host = host
        self.port = port
        self.relative = relative
        self.https = False

    def https(self, is_https=None):
        if is_https is None:
            return self.https
        else:
            self.https = is_https

    def get_url(self):
        out = HTTPS_PREFIX if self.https else HTTP_PREFIX
        out += self.host
        out += "" if self.port is None else ":%d" % self.port
        out += "" if self.relative is None else self.relative
        return out

