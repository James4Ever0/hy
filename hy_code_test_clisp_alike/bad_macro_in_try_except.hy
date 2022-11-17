(import traceback)
(try ;; wrongly use if macro. will that fuck up?
(if (= 1 1) (print "invalid if macro running!") )
(except [] (traceback.print_exc) (print "error in invalid if macro")
)
)
;; you do separate expression by parenthesis. what about invalid python object?
; this exception is raised during compile time. nothing can save you. shit.
; so you still have to capture it somehow.
;;  _get_code_from_file(run_name, path_name)
;; inside runhy. you need to patch it.