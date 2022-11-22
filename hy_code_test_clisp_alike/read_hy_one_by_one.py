
from hy.reader import HyReader
from io import StringIO
import hy.models

with open("my_bad_code.hy",'r') as f: # the read-many method. what about hy.read?
    # source_code = f.read()
    # some other value?
    # so we need to assign this value elsewhere?
    # source_code = '(print "VALUE" (try (+ 1 1) (except [] "SOME VALUE")))' # shall you return 2
    # test for the 'if' macro
    # source_code = '(if (= 1 1) (print "MATH WORKS") )' # it is just some raw expression.
    # source_code = '(if (= 1 1) (print "MATH WORK") (print "MATH SUCKS") )'
    # still it is just expression. shall you consider some transformations.
    # first test on modification.
    source_code= "FULL OF SYMBOLS"
    # check the difference?
    # source_code = "(FULL) (OF) (SYMBOLS)" # every expression is wrapped. good.
    # what about those shits not wrapped in expression (brackets)?
    # source_code = """(print "OH SHIT ANOTHER ROUND")
    # (print "CAN WE CONTINUE?" (/ 1 0))""" # the location is good.
    # source_code = """(print "OH SHIT ANOTHER ROUND")
    # (print "CAN WE CONTINUE?" (raise (Exception "SUPER SUCK BUG")))""" # the location is good.
    # it is at another line. but no damn report. no traceback?
    # yes it did return 2.
    # source_code = '(print "VALUE" (try (\\ 1 0) (except [] "SOME VALUE")))'
    # value can be obtained in this way.
    # shall you offer some option for us to execute command and return value.
    # it does work. maybe?
    filename = "<unknown>"
    # where is the traceback? i wonder.
    stream =StringIO( source_code)
    parsed_item = HyReader().parse(stream, filename) # this is the generator.
    m = hy.models.Lazy(parsed_item, protect_toplevel=False)
    # evaluate this.
    # even if you got this awesome expression, it still need to be expanded.
    # functionTrees = getFunctionForms(m,{},None)
    # breakpoint()

    # import hy.cmdline
    # val = hy.cmdline.hy_eval(m)

    # print("VAL FROM EVAL", val) #NONE.
    # print(m) # lazy.
    # you need to modify the lazy shit.
    ################EVALUATE THIS THING################
    # that might be another story.
    # for form in m:
                # do the same thing.
        # finding the appropriate form?
        # print("FORM:", form) # wrong use of macro 'if' will not raise exception for us at this time. only parser error will be raised, like premature input (inbalanced brackets).
# m = hy.models.Lazy((reader or HyReader()).parse(stream, filename))
