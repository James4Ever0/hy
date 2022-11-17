;; (from bad_py import badfunction) ;; cannot from import? wtf?
(print "about to import")
(raise (Exception "CAN TURNED INTO SOME CODE OBJECT?")) ;; 
;; you can even fail when import.
(print "IMPORT RESULT?" (import bad_py [badfunction]) );; this is the "from...import..." syntax.
;; it should raise exception really. but it does not.
;; but this is the statement to be blamed. you can import it otherwise.
; a is not defined.
(if (+ a a) '()) ; invalid syntax
;; line number is not right. please correct.
(print "imported some really bad function and about to execute")
(print "BAD FUNCTION EVAL RESULT?" (badfunction)) ; the line is extracted. but the shit is still there.