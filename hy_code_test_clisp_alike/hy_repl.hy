;; shitty overhead
;; use hy.gensym to avoid name clash.

(import traceback)
(import sys)

; but i need that fucking macro somehow
; call (hy.gensym) to get a unique symbol.

(setv minput "")
(setv leager "=> ")
(setv mretry False)
(setv mcontinue False) ; enabled when inside loop, but currently it is only avaliable when either continue or break is called.
(setv mbreak False)

;; you know parsing this shit is not just parsing this shit.
;; you might define closure.
;; shall you use the same context?

;; macro works in repl.
;; what about closure?
;; SKIP, RETRY, STOP.
;; REPLACE (REPLACE THE STATEMENT WITH YOUR OWN STATEMENT (MAYBE YOU WANT TO WRITE THAT TO DISK AS WELL))

(print "SKIP (continue execution, value as None)")
(print "RETRY (retry statement)")
(print "RAISE (raise hy.HE exception)")
(print "CONT CONTINUE (continue execution with last stored value)")

;; call it SKIP instead.
;; question: what fucking exception we are about to raise?
;; may we copy that exception?
;; raise the original exception, not exceptions inside repl.
;; define some reloading function for hy code, so we can hot patch these freaking definitions.
(setv moutput None)

(while True (try
; this expression is identical to original value.
(when mretry (setv mretry False) (setv moutput myExpression))
    (+= minput (input leager))
    (setv hytree (hy.read minput))
    (when
        (= (type hytree) hy.models.Symbol)
        (when (in hytree ['quit 'exit]) (print "use (quit) or (exit) to exit program."))
        ;; maybe you want to ban this as well.
        (when (in hytree ['SKIP]) (setv moutput None) (break))
        (when (in hytree ['CONT CONTINUE]) (break))
	(when (in hytree ['RETRY] (setv mretry True) (continue)))
	(when (in hytree ['RAISE]) (raise (hy.HE "REPL Exception")))
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
	(when
            (= (get hytree 0) ['continue])
	    (setv mcontinue True)
	    (break)
	)
	(when
            (= (get hytree 0) ['break])
	    (setv mbreak True)
	    (break)
	)
	; this depends whether the expression starts with corresponding symbol.
	(when
            (= (get hytree 0) ['return])
	    (when (= (len hytree) 1) (return))
	    (return (lfor x (cut hytree :start 1) (hy.eval x)))
	    )
(when
            (= (get hytree 0) ['yield])
	    (when (= (len hytree) 1) (yield))
	    (yield (lfor x (cut hytree :start 1) (hy.eval x)))
	    )
(when
            (= (get hytree 0) ['yield-from])
	    (when (= (len hytree) 2) (yield-from (hy.eval (get hytree 1))))
	    (print "incorrect number of arguments for 'yield-from':" (- (len hytree) 1))
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
    [hy.HE]
    (raise)
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

; do you want macro or expression? i prefer expression.

(when mcontinue (continue))
(when mbreak (break))

(print "shit?")
;it does not raise exception for ast errors. wtf?
