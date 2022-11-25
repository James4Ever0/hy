(import reloading [reloading])

(defn [reloading] shitfunc [] (return "myval"))
;; you must correct this mistake.
;; (defn [reloading] shitfunc [] (raise (Exception "I WILL RAISE SHIT OH FUCK4")))

(print "VALUE?" (shitfunc)) ;; this will fuck up. please disable all security protocol.

;; hy -L -T -K simple_reload.hy
(print "shit")
