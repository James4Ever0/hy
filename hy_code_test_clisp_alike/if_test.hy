;; (if (= 1 1) (print "shit")) ; this is if-else macro. not one single action.
;; (when (= 1 1) (print "shit"))
;; (if (= 1 1) (print "shit") (print "good"))
;; (setv hytree '())
;; (setv hytree '(exit))
;; (if (= (type hytree) hy.models.Expression)
;; (print "VAL"))
;; you like ellipsis?

(when (= (type hytree) hy.models.Expression) (when
    (= (len hytree) 1)
    ;; so you need to do things.
    (when
        (in (get hytree 0) ['quit 'exit])
        ;;   (print "program will exit")
        (do
            (exit)
            ;; real termination?
            ;;   (break)
        )
        ;; wtf is this?
        ;; that break will cause parsing to fail
    )
))
