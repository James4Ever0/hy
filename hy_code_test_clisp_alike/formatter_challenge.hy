(setv source #[[(try (+ 1 1) (except [SystemExit] (raise)) (except [] "mySignature" (import traceback) (traceback.print_exc) (print "just some error let's keep going") "USE THIS VALUE INSTEAD"))]])
(setv expression (hy.read source))
(import hyrule)
(print (hyrule.pprint expression)) ; it does not work