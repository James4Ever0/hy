(defn
    fun
    []
    (print "inside fun")
    (defn fun2 [] (print "fun2 running"))
)

(fun)
(fun2)

;; this is not defined. cannot dynamically inject shit?
;; macro can be global.
