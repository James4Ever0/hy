(import traceback)
(defn func2 [] (print "some code in func2") (try (raise (Exception "myException") (except [] (traceback.print_exc) (print "contained")))))