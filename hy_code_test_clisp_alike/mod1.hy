;; expression is evaluated. wtf?
;; the shit will not run? how do I manage some remedy?
;; () ;; sure it is getting the code, loading from file, but the exception is not caught.
;; importer._get_code_from_file
(print "ABCDEFG")
(defn func1 [] (print "CODE IN FUNC1"))
(func1); still no shit is going on.
; i think it must be the macro.

(defmacro f [ a b c ] `(~a ~b ~c)) ;; why the fuck you have newline?
;; are you sure this macro will fucking work?
; i need you to reparse the file, despite the fact it has failed.
(f print "ab" 1)
; fail to expand macro will fuck everything up. if this is is the damn file it will be doomed.
;; (if [] (1))
(print "ARE WE GOOD?") ;; not good. it is happening during parsing. not during execution. you must change that line.
;; yes it fucking works.
;; (defn funImport [] (import mod2) (mod2.func2)) ; exception is raised.
;; ;; (import mod2)
;; ;; ; it is in some kind of expression.
;; ;; (mod2.func2) ;; this time no 
;; (funImport)