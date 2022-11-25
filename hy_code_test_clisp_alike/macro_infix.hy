(defmacro infix [code]
  (quasiquote (
    (unquote (get code 1))
    (unquote (get code 0))
    (unquote (get code 2)))))

(print "val2" (infix (1 + 1)))
