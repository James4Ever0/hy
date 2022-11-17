(import bad_composition [badfunc]) ;; is this global? is this local? how the fuck we can do reloading?

;; provide "reloading" macro, recompile code and reload code all from itself?
;; and many more macros, till you get it right.
;; with extra steps. of course.

(print "CALLING BADFUNC")
(badfunc)
(print "SHIT WE MADE IT")