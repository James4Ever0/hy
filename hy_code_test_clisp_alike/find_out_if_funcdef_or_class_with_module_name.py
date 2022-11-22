def func():
    def innerfunc():
        pass
    print(innerfunc.__name__,innerfunc.__module__)

print(func.__name__, func.__module__)
func()

class mClass:
    a = 1

print(mClass.__name__, mClass.__module__)
# fucking work?
#####################
# func __main__
# innerfunc __main__
# mClass __main__