(setv q (hy.read-many "(a b) (c d) (")) ; parse error imminent
;; it is unable to unpack the shit.
;; (setv a (list q)) ; cannot use starred expression here? wtf?
; better not to unpack shit?
; what is python list, and what is list comprehension in hy?
;; (print q)
;; (for )
;; for x in q?
;; evaluate this thing.
(for [x q] (print "EXPRESSION" x)) ;; it is printing expression.
;; premature end of input. what could go wrong?