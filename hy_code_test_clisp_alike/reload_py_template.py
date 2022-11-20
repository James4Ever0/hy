from reloading import reloading # please install my fucking version.

@reloading
def testfunc():
    raise Exception('myexception will be raised.')

testfunc()