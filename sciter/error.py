u"""Sciter error classes."""


class SciterError(Exception):
    u"""Base class for Sciter exceptions."""
    pass


class ScriptError(SciterError):
    u"""Raised by runtime from calling script when script error occured (e.g. bad syntax)."""
    def __init__(self, message, script=None):
        super(ScriptError, self).__init__(self, message.replace(u"\r", u"\n"))
        self.message = message
        self.script = script

    def __repr__(self):
        return u'%s("%s") at "%s"' % (type(self).__name__, self.message.replace(u"\r", u"\n").rstrip(), self.script if self.script else u"<>")

    def __str__(self):
        return type(self).__name__ + u": " + self.message.replace(u"\r", u"\n").rstrip()
    pass


class ScriptException(ScriptError):
    u"""Raised by script by throwing or returning Error instance."""
    def __init__(self, message, script=None):
        super(ScriptException, self).__init__(message, script)
        pass
