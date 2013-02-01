

class Container(object):
    def __init__(self, web_app):
        super(Container, self).__init__()
        self.web_app = web_app
        self.elements = {}
        self.build_elements()

    def build_elements(self):
        raise NotImplementedError()

    def put(self, element):
        assert element is not None
        assert element.label is not None and len(element.label) > 0
        self.elements[element.label] = element
        return self

    def get(self, label):
        assert label is not None and len(label) > 0
        return self.elements[label]

    def get_elements(self, clss=None, required=None):
        l = []

        if clss is not None:
            l = [v for v in self._map.values() if isinstance(v, clss)]
        else:
            l = [v for v in self._map.values()]

        if required is None:
            return l
        else:
            return [v for v in l if v.required == required]

