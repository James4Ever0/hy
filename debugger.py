import hy.models

from hy.models import Symbol as S, Expression as E, List as L, String as STR

def myTryExceptMacro(myExpression, signature='mySignature',checkExpression=False, 
# skipAssertions = False
topLevel=False, #indicate this is toplevel try-except. no more reprievment. # you may rewrap this thing.
allowed_exception_symbols = [S('SystemExit')], # make sure these errors are builtin. PLEASE!
skipAssertions=True ,# to make it right?
) :  # what do you want to convert?
    # what is the damn attribute of this damn shit?
    # test if this is the damn thing.
    # this is expression in deed.
    if checkExpression:
        if type(myExpression) == E:
            try:
                valSignature = myExpression[2][2]
                if valSignature == STR(signature):
                    return myExpression
            except:
                pass
    try:
        valfirst = myExpression[0]
        testskip = (valfirst == S('except') or valfirst == S('finally')) or ((valfirst == S('assert')) if skipAssertions else False)
        if testskip:
            return myExpression
    except:
        # empty expression passed? damn...
        pass
    # did you have traceback?
    # you raise these exceptions instead of catching them.
    # default is SystemExit. but that could fuck up. you may need to disable them in source code but allow them in hy repl, maybe in debug repl too?
    myAllowedExceptions = []
    for sym in allowed_exception_symbols:
        if type(sym) == str:
            sym = hy.models.Symbol(str)
        aexp = E([S('except'), L([sym]), E([S('raise')])])
        myAllowedExceptions.append(aexp)
    baseExpression = [S('try'),myExpression]+myAllowedExceptions+[E([S('except'), L(), STR(signature),E([S('import'), S('traceback')]), E([S('traceback.print_exc')]),E([S('print'), STR("just some error let's keep going")]), STR('USE THIS VALUE INSTEAD')])]
    val = E(baseExpression) # no value returned?
    # print('just before we return this evil thing...')
    # breakpoint()
    # for better tracking of error.
    val._start_column = myExpression._start_column
    val._start_line = myExpression._start_line
    val._end_column = myExpression._end_column
    val._end_line = myExpression._end_line
    return val