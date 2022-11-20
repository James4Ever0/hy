(print "HELLO WORLD5")
(print "HELLO WORLD2")
(defn shit [] (raise (Exception "SHIT"))) ;; most recent call last?
(shit)
(raise (Exception "SHIT"))
(print "HELLO WORLD3")
(print "HELLO WORLD3") ;; maybe you should enable that shit manually.
