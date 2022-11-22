(import inspect)

;; how to reload this definition? parse the definition? transform this shit into ast?

(print "SHIT! WTF IS GOING ON?")
(print "SHIT! WTF IS GOING ON?")

;; HyASTCompiler?
;; retrieve this thing. use this thing!
;; what if you are using some unknown macros?

(defn
    reloading_hy ;; a decorator.
    [func] ;; retry till success.
    ;; there is no type hint in hy. fucking hell. what a creep.
    ;; load the damn fucking definition, just like reloading.
    (setv mstack (inspect.stack))
    (setv myStack (get mstack 1)) ;; what fucking stack we have?
    ;; frame? fstack?
    ;; we can retrieve this stack number.
    (print)
    ;; how the fuck you retrieve this shit.
    (print "MY STACK?" myStack) ;; i guess this stack is not good.
    (print) ;; can you retrieve module information from either class definition or function definition? let's use simple python code to find out.
    ;; (print (dir func)) ;; this is a function. maybe async?
    ;; ['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    (print "___________")
    ;; obtain code object?
    ;; myerrorfunc __main__
    ;; sort the nearest definition around the shit.
    (print func.__name__ func.__module__ func.__code__) ; seek for name this damn function.
    ;; this is the damn name. but how to seek for this function?
    ;; check the damn definition.
    ;; why not fucking works?
    (defn inner_func [ #* args #** kwargs ] ;; does not fucking work?
        (print "executing code")
        (func #* args #** kwargs) ;; remove this decorator when running, please.
        ;; oh really?
    )
    ;; (func)
    (return inner_func)
)

;; man we are doing shit. if intepreter flag is set, we are fucked.
(defn [reloading_hy] myerrorfunc [] (raise (Exception "SHIT")))

(myerrorfunc)
(print "FUCKING SHIT2")
(raise (Exception "SHIT")) ;; cannot raise exception! not able to disable the protection in some way.
(raise (Exception "SHIT"))
;; (raise (Exception "SHIT"))
(print "SHIT2")