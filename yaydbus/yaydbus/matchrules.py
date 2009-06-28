class MatchRule(dict):
    def add_match(self, key, value):
        self[key] = value

    def to_dbus(self):
        return ','.join("%s='%s'" % (key, value) for key, value in self.iteritems())
