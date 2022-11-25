(defn mret [] (hy.eval (hy.read "(return 1)")))

;(print "val" (mret))

(try (print "abc") (return 1) (except [] (print "oh yeah")))
