
;____

(try
    (try
        (defn fun [] (try
            (do
                (try
                    (try
                        (try
                            (/ 1 0)
                            (except [SystemExit] (raise))
                            (except
                                []
                                "mySignature"
                                (import traceback)
                                (traceback.print_exc)
                                (print "just some error let's keep going")
                                "USE THIS VALUE INSTEAD"
                            )
                        )
                        (try
                            (trivial_func (try
                                (/ 1 0)
                                (except [SystemExit] (raise))
                                (except
                                    []
                                    "mySignature"
                                    (import traceback)
                                    (traceback.print_exc)
                                    (print "just some error let's keep going")
                                    "USE THIS VALUE INSTEAD"
                                )
                            ))
                            (except [SystemExit] (raise))
                            (except
                                []
                                "mySignature"
                                (import traceback)
                                (traceback.print_exc)
                                (print "just some error let's keep going")
                                "USE THIS VALUE INSTEAD"
                            )
                        )
                        (try
                            (assert (try
                                (/ 1 0)
                                (except [SystemExit] (raise))
                                (except
                                    []
                                    "mySignature"
                                    (import traceback)
                                    (traceback.print_exc)
                                    (print "just some error let's keep going")
                                    "USE THIS VALUE INSTEAD"
                                )
                            ))
                            (except [SystemExit] (raise))
                            (except
                                []
                                "mySignature"
                                (import traceback)
                                (traceback.print_exc)
                                (print "just some error let's keep going")
                                "USE THIS VALUE INSTEAD"
                            )
                        )
                        (except [] (try
                            (print "THIS EXCEPTION IS WRAPPED")
                            (except [SystemExit] (raise))
                            (except
                                []
                                "mySignature"
                                (import traceback)
                                (traceback.print_exc)
                                (print "just some error let's keep going")
                                "USE THIS VALUE INSTEAD"
                            )
                        ))
                    )
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                )
                (try
                    (assert (try
                        (= 1 0)
                        (except [SystemExit] (raise))
                        (except
                            []
                            "mySignature"
                            (import traceback)
                            (traceback.print_exc)
                            (print "just some error let's keep going")
                            "USE THIS VALUE INSTEAD"
                        )
                    ))
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                )
            )
            (except [SystemExit] (raise))
            (except
                []
                "mySignature"
                (import traceback)
                (traceback.print_exc)
                (print "just some error let's keep going")
                "USE THIS VALUE INSTEAD"
            )
        ))
        (except [SystemExit] (raise))
        (except
            []
            "mySignature"
            (import traceback)
            (traceback.print_exc)
            (print "just some error let's keep going")
            "USE THIS VALUE INSTEAD"
        )
    )
    (except [SystemExit] (raise))
    (except
        []
        "mySignature"
        (import traceback)
        (traceback.print_exc)
        (print "just some error let's keep going")
        "USE THIS VALUE INSTEAD"
    )
)



;____

(try
    [
        1
        2
        3
        (try
            (+ 1 1)
            (except [SystemExit] (raise))
            (except
                []
                "mySignature"
                (import traceback)
                (traceback.print_exc)
                (print "just some error let's keep going")
                "USE THIS VALUE INSTEAD"
            )
        )
        (try
            (try
                (try
                    (+ 1 0)
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                )
                (except [] (try
                    (print "SHIT")
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                ))
            )
            (except [SystemExit] (raise))
            (except
                []
                "mySignature"
                (import traceback)
                (traceback.print_exc)
                (print "just some error let's keep going")
                "USE THIS VALUE INSTEAD"
            )
        )
    ]
    (except [SystemExit] (raise))
    (except
        []
        "mySignature"
        (import traceback)
        (traceback.print_exc)
        (print "just some error let's keep going")
        "USE THIS VALUE INSTEAD"
    )
)



;____

(try
    a.b.c
    (except [SystemExit] (raise))
    (except
        []
        "mySignature"
        (import traceback)
        (traceback.print_exc)
        (print "just some error let's keep going")
        "USE THIS VALUE INSTEAD"
    )
)



;____

(try
    {1 3 4 #{
        :1 mdict
        :2 mdict
        :3 mdict
        :4 mdict
        :5 (try
            (+ 1 1)
            (except [SystemExit] (raise))
            (except
                []
                "mySignature"
                (import traceback)
                (traceback.print_exc)
                (print "just some error let's keep going")
                "USE THIS VALUE INSTEAD"
            )
        )
        :6 (try
            (try
                (try
                    (+ 1 0)
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                )
                (except [] (try
                    (print "SHIT")
                    (except [SystemExit] (raise))
                    (except
                        []
                        "mySignature"
                        (import traceback)
                        (traceback.print_exc)
                        (print "just some error let's keep going")
                        "USE THIS VALUE INSTEAD"
                    )
                ))
            )
            (except [SystemExit] (raise))
            (except
                []
                "mySignature"
                (import traceback)
                (traceback.print_exc)
                (print "just some error let's keep going")
                "USE THIS VALUE INSTEAD"
            )
        )
    }}
    (except [SystemExit] (raise))
    (except
        []
        "mySignature"
        (import traceback)
        (traceback.print_exc)
        (print "just some error let's keep going")
        "USE THIS VALUE INSTEAD"
    )
)



;____

(try
    "some dumb string"
    (except [SystemExit] (raise))
    (except
        []
        "mySignature"
        (import traceback)
        (traceback.print_exc)
        (print "just some error let's keep going")
        "USE THIS VALUE INSTEAD"
    )
)


