class UnknownStrategy(Exception):
    def __init__(self, msg, *args, **kwargs):
        super(UnknownStrategy, self).__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self):
        return self.msg

