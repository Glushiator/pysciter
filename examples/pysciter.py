u"""More complex PySciter sample."""

from __future__ import absolute_import
import sciter

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super(Frame, self).__init__(ismain=True, uni_theme=True)
        pass

    def on_subscription(self, groups):
        # subscribing only for scripting calls and document events
        from sciter.event import EVENT_GROUPS
        return EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT | EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL

    def on_script_call(self, name, args):
        # script calls
        print name, u"called from script"
        return self.dispatch(name, args)


    ## @name The following functions are called from scripts:
    @sciter.script
    def PythonCall(self, arg):
        return u"Pythonic window (%s)" % unicode(arg)

    @sciter.script
    def GetNativeApi(self):

        def on_add(a, b):
            return a + b

        def on_sub(a, b):
            raise Exception(u"sub(%d,%d) raised exception" % (a, b))

        api = { u'add': on_add,              # plain function
                u'sub': on_sub,              # raised exception will propagated to script
                u'mul': lambda a,b: a * b,   # lambdas support
                }
        return api

    @sciter.script
    def ScriptCallTest(self):
        print u"calling 'hello'"
        answer = self.call_function(u'hello', u"hello, python")
        print u"call answer: ", answer

        print u"get and call 'hello'"
        answer = self.eval_script(u'hello')
        answer = answer.call(u'argument', name=u'on_script_call')
        print u"get answer: ", answer

        print u"eval 'hello'"
        answer = self.eval_script(u'hello("42");')
        print u"eval answer: ", answer

        try:
            print u"\ncalling 'raise_error'"
            answer = self.call_function(u'raise_error', 17, u'42', False)
            print u"expected ScriptError"
        except sciter.ScriptError, e:
            print u"answer: ", unicode(e)


        try:
            print u"\nget and call 'raise_error'"
            answer = self.eval_script(u'raise_error')
            answer = answer.call(u'argument', name=u'on_script_call')
            print u"expected ScriptError"
        except sciter.ScriptError, e:
            print u"answer: ", unicode(e)

        try:
            print u"\ncalling unexisting function"
            answer = self.call_function(u'raise_error2')
            print u"expected ScriptError"
        except sciter.ScriptError, e:
            print u"answer: ", unicode(e)
        return True

    ## @}

# end


if __name__ == u'__main__':
    sciter.runtime_features(allow_sysinfo=True)

    import os
    htm = os.path.join(os.path.dirname(__file__), u'pysciter.htm')
    frame = Frame()
    frame.load_file(htm)
    frame.run_app()
