(defn
    fun
    ; disable-protection
    [];; empty input
    ;; toplevel shall always be protected, no matter what, unless manually disabled by comments.
    ;; the only way to disable protection within is to try...except some code blocks. if this fails, it will still be captured.
    ;; or just use python to write libraries for hy.
    ;; i personally hate the idea to disable protection with comments. doesn't mean shit.
    (do
        ;; worst practice! won't implement.
        ; disable-protection
        ;; expressions inside this try...except shall not be re-wrapped.
        (try
            (/ 1 0)
            (trivial_func (/ 1 0))
            (assert (/ 1 0)) ; this is definitely not wrapped, if our design is correct.
            (except [] (print "THIS EXCEPTION IS WRAPPED"))
        )
        (assert (= 1 0));;this is not wrapped. no it is wrapped and it is fucked.
    )
)

; now check the legitimacy of this shit.

[
    1
    2
    3
    (+ 1 1)
    (try (+ 1 0) (except [] (print "SHIT")))
]
a.b.c
{1 3 4 #{
    :1 mdict
    :2 mdict
    :3 mdict
    :4 mdict
    :5 (+ 1 1)
    :6
    (try (+ 1 0) (except [] (print "SHIT")))
}}

"some dumb string"