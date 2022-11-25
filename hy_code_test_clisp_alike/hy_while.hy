(print
    "value?"
    (do
    (setv mretval None)
    (while True (try
        (raise (Exception "shit"))
        (except [] (setv mretval "return val") (break))
    )) mretval)
)

