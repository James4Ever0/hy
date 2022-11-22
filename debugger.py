import hy.models

from hy.models import Symbol as S, Expression as E, List as L, String as STR


def showStackTrace(myExpression, disable_showstack=False):  # warning! please do copy the line metadata.
    # only triggered when toplevel protection is disabled.
    # let's fuck this up...
    if disable_showstack:
        return myExpression # for whatever reason this shit need to deal with.
    baseExpression = E(
        [S("try"), myExpression]
        + [
            E(
                [
                    S("except"),
                    L([S("SystemExit")]),
                   # E(
                   #     [
                   #         S("pass"),
                   #     ]
                   # ),
                    E(
                        [
                            S(
                                "raise"
                            ),  # finally raise what? what the fuck do you want? what the shit do you want?
                        ]
                    ),
                ]
            )
        ]
        + [
            E(
                [
                    S("except"),
                    L(),
                    E([S("import"), S("traceback")]),
                    E([S("traceback.print_exc")]),
                    E(
                        [
                            S(
                                "raise"
                            ),  # finally raise what? what the fuck do you want? what the shit do you want?
                        ]
                    ),
                ]
            )
        ]
        # + [
        #     E(
        #         [
        #             S("finally"),
        #             E(
        #                 [
        #                     S("raise"), # finally raise what? what the fuck do you want? what the shit do you want?
        #                 ]
        #             ),
        #         ]
        #     )
        # ]
    )

    baseExpression._start_column = myExpression._start_column
    baseExpression._start_line = myExpression._start_line
    baseExpression._end_column = myExpression._end_column
    baseExpression._end_line = myExpression._end_line
    return baseExpression

def checkBlacklist(myExpression, blacklist=[S('unpack-iterable'), S('unpack-mapping')]):
    if type(myExpression) == E:
        try:
            firstSym = myExpression[0]
            if firstSym in blacklist:
                return False
        except:
            pass
        return True
    return False


def checkAuthenticTryExcept(myExpression, signature="mySignature"):
    sig_try, sig_authentic = False, False
    if type(myExpression) == E:
        try:
            sig_try = myExpression[0] == S("try")
            valSignature = myExpression[-1][2]  # the last expression! fuck.
            if valSignature == STR(signature):
                sig_authentic = True
        except:
            pass
    return sig_try, sig_authentic


# if without toplevel protection, we must trace this shit.
def myTryExceptMacro(
    myExpression,
    signature="mySignature",
    checkExpression=False,
    # skipAssertions = False
    topLevel=False,  # indicate this is toplevel try-except. no more reprievment for skipAssertions. # you may rewrap this thing.
    # but it fucking have no use! only use is for skipAssertions!
    allowed_exception_symbols=[
        S("SystemExit")
    ],  # make sure these errors are builtin. PLEASE!
    skipAssertions=False,  # to make it right?
    # why skip assertions? no you should not skip assertions? who the fuck is calling us?
    # you should reload the method definition from somewhere?
    # talking of toplevel is not right.
    # why the fuck you want to skip assertions? what if it fucking cause you trouble outside of function definition?
    # if you don't assert shit, it will still break shit and you don't have chance to correct it properly.
):  # what do you want to convert?
    # what is the damn attribute of this damn shit?
    # test if this is the damn thing.
    # this is expression in deed.
    # this will check if this is 
    if not topLevel:
        sig_blacklist_passed = checkBlacklist(myExpression)
        if not sig_blacklist_passed:
            return myExpression

    if checkExpression:
        sigs = checkAuthenticTryExcept(myExpression, signature=signature)
        if all(sigs):
            return myExpression
    try:
        valfirst = myExpression[0]
        testskip = (valfirst == S("except") or valfirst == S("finally")) or (
            (valfirst == S("assert")) if ((not topLevel) and skipAssertions) else False
        )
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
        aexp = E([S("except"), L([sym]), E([S("raise")])])
        myAllowedExceptions.append(aexp)
    baseExpression = (
        [S("try"), myExpression]
        + myAllowedExceptions
        + [
            E(
                [
                    S("except"),
                    L(),
                    STR(signature),
                    E([S("import"), S("traceback")]),
                    E([S("traceback.print_exc")]),
                    E([S("print"), STR("just some error let's keep going")]),
                    STR("USE THIS VALUE INSTEAD"),
                ]
            )
        ]
    )
    val = E(baseExpression)  # no value returned?
    # print('just before we return this evil thing...')
    # breakpoint()
    # for better tracking of error.
    val._start_column = myExpression._start_column
    val._start_line = myExpression._start_line
    val._end_column = myExpression._end_column
    val._end_line = myExpression._end_line
    return val
