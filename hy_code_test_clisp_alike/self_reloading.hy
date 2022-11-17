;; how do you rewrite this bad function?

(defn ;; parse this shit again please?
    badfunc
    []
    (raise (Exception "SHIT"))
)

(defn hasclosure [] 
(defn closurefunc [] (raise (Exception "CLOSURE SHIT")))

(print "CLOSURE?" closurefunc.__code__ closurefunc.__name__)
)

;; (setv filepath "/Users/jamesbrown/Desktop/works/hy_code_test_clisp_alike/")
;; but you should get the picture. do you?

(print "val returned:" (when
    (= __name__ "__main__")
    ;; (+ 1 1)
    ;; "val"
    ;; (print (dir badfunc))
    (print "JUST BEFORE WE INSPECT")
    ;; badfunc is function here. so consider to reload that as function.
    ;; handle it differently.
    (print badfunc.__code__ badfunc.__name__);; how do we obtain similar info for us?
    ()
    ;; hy code -> ast -> code
    ;; it has globals.
    ;; ['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    (print (dir badfunc.__code__ ))
    (breakpoint)
;; ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_posonlyargcount', 'co_stacksize', 'co_varnames', 'replace']
)) ;; doesn't matter. keep going!
