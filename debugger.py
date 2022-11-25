import hy.models

from hy.models import Symbol as S, Expression as E, List as L, String as STR


class HyTryExceptException(Exception):
    pass

def importReloading(myExpression):
    try:
        if isinstance(myExpression,E):
            if myExpression[0] == S('do'):
                mexp= myExpression[1]
                if mexp[0]==S('import') and mexp[1] ==S('reloading') and mexp[2][0] == S('reloading'):
                    return myExpression
    except:
        pass
    importExpression=E([S('import'),S('reloading'), L([S('reloading')])
        ])
    baseExpression=E([S('do'), importExpression,myExpression
        ])
    baseExpression._start_column = myExpression._start_column
    baseExpression._start_line = myExpression._start_line
    baseExpression._end_column = myExpression._end_column
    baseExpression._end_line = myExpression._end_line
    return baseExpression


def checkDefnode(myExpression):
    mdefsyms=[hy.models.Symbol(n) for n in ['defn','defclass']]
    hasDeclist=False
    sig=False
    try:
        firstsym=myExpression[0]
        if firstsym in mdefsyms:
            sig=True
            #now check if we have decorator list.
            if isinstance(myExpression[1], L):
                hasDeclist=True
    except:
        pass
    return sig, hasDeclist

def checkReloading(myExpression):# this is different. if this is not def node, not an expression, default return True
    #does it have reloading recorator?
    declist=myExpression[1]
    if not isinstance(declist, L):
        return True
    else:
        for dec in declist:
            if dec == S('reloading'): 
                return True
            elif isinstance(dec, E):
                try:
                    if dec[0] == S('reloading'):
                        return True
                except:
                    pass
        return False
    return True

def getMeta(mexp):
    return mexp.start_column, mexp.start_line, mexp.end_column, mexp.end_line, mexp.__module__

def insertReloadingDecorator(mexp):
    subelem=[elem for elem in mexp]
    mdeclist=subelem[1]
    needInsert=False
    msym=S('reloading')
    if not isinstance(mdeclist, L):
        msc, msl, _,_, mm=getMeta(subelem[0])
        _,_,mec, mel, mm=getMeta(subelem[1])

        msym.start_column,msym.start_line,msym.end_column, msym.end_line, msym.module=msc,msl, mec, mel, mm

        mdeclist=L([msym])
        mdeclist.start_column,mdeclist.start_line,mdeclist.end_column, mdeclist.end_line, mdeclist.module=msc,msl, mec, mel, mm
        needInsert=True
    else:

        msubdecs=[e for e in mdeclist]
        #final element?
        if len(msubdecs)==0:
            msym.start_column, msym.start_line, msym.end_column, msym.end_line, msym.__module__=getMeta(mdeclist)
        else:
            msc, msl,_,_, mm=getMeta(msubdecs[-1])
            _,_,mec,mel, mm=getMeta(mdeclist)
            msym.start_column, msym.start_line, msym.end_column, msym.end_line, msym.__module__=msc, msl, mec, mel, mm
        # now append shit. please!
        msubdecs.append(msym)
        mdeclist2=L(msubdecs)

        mdeclist2.start_column, mdeclist2.start_line, mdeclist2.end_column, mdeclist2.end_line, mdeclist2.__module__=getMeta(mdeclist)
        mdeclist=mdeclist2

    if needInsert:
        subelem.insert(1,mdeclist)
    else:
        subelem[1] = mdeclist

    mexp2=E(subelem)
    mexp2.start_column, mexp2.start_line, mexp2.end_column, mexp2.end_line, mexp2.__module__=getMeta(mexp)
    return mexp2

def addReloadingDecorator(myExpression,hasDeclist=False):# has it or not we will not care.
#    hasReloading=checkReloading(myExpression)
#    if not hasReloading:
    myExpression=insertReloadingDecorator(myExpression)
    return myExpression

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

def checkBlacklist(myExpression, blacklist=[S('unpack-iterable'), S('unpack-mapping'), 
    #S('break'), S('continue'), 
    S('except'), S('finally')]):
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
            S("SystemExit"), S('hy.HE')
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
                        #E([S("print"), STR("just some error let's keep going")]),
                        E([S("print"), STR("Entering debug REPL")]),
                        #STR("USE THIS VALUE INSTEAD"),
                        ]
                    )
                ]
            )
    # mloop=E([S('while'), S('True') ])
    # how to re-execute?

    # wrap inside a do statement.
    # make sure the variable identifier is unique somehow?
    val = E(baseExpression)  # no value returned?
    # print('just before we return this evil thing...')
    # breakpoint()
    # for better tracking of error.
    val._start_column = myExpression._start_column
    val._start_line = myExpression._start_line
    val._end_column = myExpression._end_column
    val._end_line = myExpression._end_line
    return val
