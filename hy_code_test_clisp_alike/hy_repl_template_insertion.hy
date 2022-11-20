;; shitty overhead
;; use hy.gensym to avoid name clash.

(import traceback)
(import sys)

;; simply cannot continue at the statement do you?
;; you can continue doing this. it doesn't harm.
;; (try (hy.read "(") (except [] (traceback.print_exc) (print "exception in parsing code")))
; should you continue to type more things.

(setv minput "")
(setv leager "=> ")

;; you know parsing this shit is not just parsing this shit.
;; you might define closure.
;; shall you use the same context?

(print "ENTERING DEBUGGER");;  you should at least know the last statement.

; let's define a macro.
; what about closure?

(defmacro mym [b] `(print ~b))

(print "RUNNING MACRO")
(mym "MY NEW MACRO WORKS")

;; macro works in repl.
;; what about closure?
;; SKIP, RETRY, STOP.
;; RELOAD (RELOAD DEFINITION FROM DISK)
;; REPLACE (REPLACE THE STATEMENT WITH YOUR OWN STATEMENT (MAYBE YOU WANT TO WRITE THAT TO DISK AS WELL))

(print "SKIP (continue execution to next line)")

;; call it SKIP instead.
;; question: what fucking exception we are about to raise?
;; may we copy that exception?
;; raise the original exception, not exceptions inside repl.
;; define some reloading function for hy code, so we can hot patch these freaking definitions.


;; this damn repl loop, you may want to simplify it a little bit with macro?

(while True (try
    (+= minput (input leager))
    (setv hytree (hy.read minput))
    ;; then we execute this.
    ;; (unquote hytree) ;; unquote not allowed?
    (when
        (= (type hytree) hy.models.Symbol)
        (when (in hytree ['quit 'exit]) (print "use (quit) or (exit) to exit program."))
        ;; maybe you want to ban this as well.
        (when (in hytree ['SKIP]) (break))
        ;; does not raise exception.
    )
    ;; ______________SHIT________________
    (when (= (type hytree) hy.models.Expression) (when
        (= (len hytree) 1)
        ;; so you need to do things.
        (when
            (in (get hytree 0) ['quit 'exit])
            (do
                ;; (print "termination imminent")
                ;; (breakpoint)
                (sys.exit)
                ;; real termination?
                (break)
            )
            ;; wtf is this?
        )
    ))
    ;; ______________SHIT________________
    ;; if it is not expression, better print it.
    (setv moutput (hy.eval hytree))
    (when (!= moutput None) (print moutput))
    ;; default behavior? yes?
    ;; what does this even mean to the inner function?
    ;; use unquote?
    ;; check if python is still alive?
    ;; if decide to quit, terminate the thing.
    (setv leager "=> ")
    (setv minput "")
    ;; why you keep on going?
    (except
        [hy.reader.exceptions.PrematureEndOfInput]
        (setv leager "... ")
    )
    (except
        [SystemExit];; are you sure you want to skip this freaking error?
        (sys.exit)
        ;; this will terminate the program. really?
        (break)
    )
    (except
        []
        ;; if you intentionally want to raise shit, we will do it.
        (traceback.print_exc)
        (setv minput "")
        (setv leager "=> ")
    )
    ;; all other special shits.
))

(print "what you want to do after this line?")
(breakpoint)

;; shit man what the fuck
;; shitty aftermath

