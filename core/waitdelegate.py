

class WaitDelegate(object):
    def __init__(self):
        super(WaitDelegate, self).__init__()

    def wait(self):
        raise NotImplementedError()
