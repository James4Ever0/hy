(print "HELLO WORLD5")
(print "HELLO WORLD2")
(defn shit [] (raise (Exception "SHIT"))) ;; most recent call last?

(defn [abc] s [] (print "a"))
(defn [abc reloading] s1 [] (print "a"))
(defn [abc reloading mdef] s2 [] (print "a"))
(shit)
(raise (Exception "SHIT"))
(print "HELLO WORLD3")
(print "HELLO WORLD3") ;; maybe you should enable that shit manually.

(defclass mclass []
(defn classm [] (print "class method"))
)

(defn [(reloading :every 3)] mymethod [] (print "from mymethod"))
