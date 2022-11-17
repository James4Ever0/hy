(setv expression '(quit))
;; (print (dir expression))
(print (list expression))
;; [hy.models.Symbol('quit')]
;; now we have it. you dumb shit.
(print (get expression 0)) ;; list index out of range? or some sort of shit.
;; just a symbol. damn.
;; but we really need to check if python exits.
(print "length:" (len expression))