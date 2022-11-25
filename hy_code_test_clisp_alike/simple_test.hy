(print "HELLO WORLD5")
(print "HELLO WORLD2")
(defn shit [] (raise (Exception "SHIT"))) ;; most recent call last?
;wtf is going on?
(shit)
(raise (Exception "SHIT3"))
(raise (Exception "SHIT2"))
(print "HELLO WORLD3")
(print "HELLO WORLD4") ;; maybe you should enable that shit manually.
