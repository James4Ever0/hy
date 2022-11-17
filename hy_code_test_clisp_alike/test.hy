;; (import somefunction)
(import traceback)

; make it foreign.
(print "where is the exception?")
;; the most important feature in (common) lisp is macro. other shits, doesn't matter so much.
;; does def work as expected?
;; (def myfunc2 [ val ] (print val) 2) ;; this def is not working, since the macro is not loaded.
;; (print (myfunc "myfunc2 value"))
; (somefunction.func)
; no execute, no shit.
; start a repl anywhere?
; how do you reload definition?
; will macro be overloaded?
; but does all codesection need to be fitted into one single line? doubt that.
;; shit. macro is recursive in this sense.
;; do not use scheme formatter. it is not equivalent to hy.
(defmacro def [f p c] `(defn ~f ~p (try ~c (except [] (print "error caught")))))
; all positional arguments.
;; (def mysafefunc [] (print "safe function called")) ; what the fuck
;; now it is macro?
;; hy.errors.HyMacroExpansionError: 
;; so you do have someshit to say.
;; (defn mysafefunc [] (raise (Exception "shit happened")))
(def mysafefunc [] (raise (Exception "shit happened")))
;; can you eval this function?
;; it does show the line where this thing goes wrong.
;; (raise (Exception "shit"))
;; what if there's some shit happening?
(mysafefunc)
;; (import hy)
;; still accessible?
;; yes. no need to import hy.
;; (.run (hy.cmdline.HyREPL [:locals (locals)])) ; well does this work?
; not defined? shit?
;; io operation on closed file?
(while
 True
 ;; will it succeed?
 (try
  (setv myvar (hy.read (input "=> ")))
  (if (= myvar 'CONTINUE) (print "CONTINUE EXECUTION") (continue))
            (except [] (traceback.print_exc) (print "you have error in repl"))))
;; no printing on "it is good?" just exit? exit what?
(print "it is good")
