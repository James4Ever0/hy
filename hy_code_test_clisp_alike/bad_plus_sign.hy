;; +
;; this test is too hard for you?
+
;; hyx_Xplus_signX
(try + (except [] (print "GOOD")))
;; is that what you want?
(try (print +) (except [] (print "FANTASTIC"))) ; your wrapper will fuck up everything.
;; expression is not your place to wrap shit around.
;; do not wrap around "EXCEPT" "FINALLY" Expressions.

(print "WE ARE GOLDEN")