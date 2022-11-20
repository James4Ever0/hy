(import inspect)

(defn
    reloading_hy ;; a decorator.
    [func] ;; retry till success.
    ;; there is no type hint in hy. fucking hell. what a creep.
    ;; load the damn fucking definition, just like reloading.
    (setv mstack (inspect.stack))
    (setv myStack (get mstack 1)) ;; what fucking stack we have?
    ;; frame? fstack?
    (print)
    ;; how the fuck you retrieve this shit.
    (print "MY STACK?" myStack) ;; i guess this stack is not good.
    (print)
    ;; (print (dir func)) ;; this is a function. maybe async?
    ;; ['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    (print "___________")
    ;; obtain code object?
    ;; myerrorfunc __main__
    (print func.__name__ func.__module__ func.__code__) ; seek for name this damn function.
    (defn inner_func
        [#* args #** kwargs]
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