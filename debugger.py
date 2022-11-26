import hy.models

from hy.models import (
    Symbol as S,
    Expression as E,
    List as L,
    String as STR,
    Keyword as K,
    Integer as I,
)


class HyTryExceptException(Exception):
    pass


def importReloading(myExpression):
    try:
        if isinstance(myExpression, E):
            if myExpression[0] == S("do"):
                mexp = myExpression[1]
                if (
                    mexp[0] == S("import")
                    and mexp[1] == S("reloading")
                    and mexp[2][0] == S("reloading")
                ):
                    return myExpression
    except:
        pass
    importExpression = E([S("import"), S("reloading"), L([S("reloading")])])
    baseExpression = E([S("do"), importExpression, myExpression])
    baseExpression._start_column = myExpression._start_column
    baseExpression._start_line = myExpression._start_line
    baseExpression._end_column = myExpression._end_column
    baseExpression._end_line = myExpression._end_line
    return baseExpression


def checkDefnode(myExpression):
    mdefsyms = [hy.models.Symbol(n) for n in ["defn", "defclass"]]
    hasDeclist = False
    sig = False
    try:
        firstsym = myExpression[0]
        if firstsym in mdefsyms:
            sig = True
            # now check if we have decorator list.
            if isinstance(myExpression[1], L):
                hasDeclist = True
    except:
        pass
    return sig, hasDeclist


def checkReloading(
    myExpression,
):  # this is different. if this is not def node, not an expression, default return True
    # does it have reloading recorator?
    declist = myExpression[1]
    if not isinstance(declist, L):
        return True
    else:
        for dec in declist:
            if dec == S("reloading"):
                return True
            elif isinstance(dec, E):
                try:
                    if dec[0] == S("reloading"):
                        return True
                except:
                    pass
        return False
    return True


def getMeta(mexp):
    return (
        mexp.start_column,
        mexp.start_line,
        mexp.end_column,
        mexp.end_line,
        mexp.__module__,
    )


def insertReloadingDecorator(mexp):
    subelem = [elem for elem in mexp]
    mdeclist = subelem[1]
    needInsert = False
    msym = S("reloading")
    if not isinstance(mdeclist, L):
        msc, msl, _, _, mm = getMeta(subelem[0])
        _, _, mec, mel, mm = getMeta(subelem[1])

        (
            msym.start_column,
            msym.start_line,
            msym.end_column,
            msym.end_line,
            msym.module,
        ) = (msc, msl, mec, mel, mm)

        mdeclist = L([msym])
        (
            mdeclist.start_column,
            mdeclist.start_line,
            mdeclist.end_column,
            mdeclist.end_line,
            mdeclist.module,
        ) = (msc, msl, mec, mel, mm)
        needInsert = True
    else:

        msubdecs = [e for e in mdeclist]
        # final element?
        if len(msubdecs) == 0:
            (
                msym.start_column,
                msym.start_line,
                msym.end_column,
                msym.end_line,
                msym.__module__,
            ) = getMeta(mdeclist)
        else:
            msc, msl, _, _, mm = getMeta(msubdecs[-1])
            _, _, mec, mel, mm = getMeta(mdeclist)
            (
                msym.start_column,
                msym.start_line,
                msym.end_column,
                msym.end_line,
                msym.__module__,
            ) = (msc, msl, mec, mel, mm)
        # now append shit. please!
        msubdecs.append(msym)
        mdeclist2 = L(msubdecs)

        (
            mdeclist2.start_column,
            mdeclist2.start_line,
            mdeclist2.end_column,
            mdeclist2.end_line,
            mdeclist2.__module__,
        ) = getMeta(mdeclist)
        mdeclist = mdeclist2

    if needInsert:
        subelem.insert(1, mdeclist)
    else:
        subelem[1] = mdeclist

    mexp2 = E(subelem)
    (
        mexp2.start_column,
        mexp2.start_line,
        mexp2.end_column,
        mexp2.end_line,
        mexp2.__module__,
    ) = getMeta(mexp)
    return mexp2


def addReloadingDecorator(
    myExpression, hasDeclist=False
):  # has it or not we will not care.
    #    hasReloading=checkReloading(myExpression)
    #    if not hasReloading:
    myExpression = insertReloadingDecorator(myExpression)
    return myExpression


def showStackTrace(
    myExpression, disable_showstack=False
):  # warning! please do copy the line metadata.
    # only triggered when toplevel protection is disabled.
    # let's fuck this up...
    if disable_showstack:
        return myExpression  # for whatever reason this shit need to deal with.
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


def checkBlacklist(
    myExpression,
    blacklist=[
        S("unpack-iterable"),
        S("unpack-mapping"),
        # S('break'), S('continue'),
        S("except"),
        S("quasiquote"),
        S("defmacro"),
        S('unquote-splice'),
        S('else'), # follow the damn doc?
        S('except*'),
        S("unquote"),
        S("finally"),
        S("annotate"),
    ],
):
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

def stripTryExcept(exp):
    s0,s1=checkAuthenticTryExcept(exp)
    if s0 and s1:
        return exp[1]
    return exp


# if without toplevel protection, we must trace this shit.
def myTryExceptMacro(
    myExpression,
    signature="mySignature",
    checkExpression=False,
    # skipAssertions = False
    topLevel=False,  # indicate this is toplevel try-except. no more reprievment for skipAssertions. also do catch hy.HE for whatever reason.
    # you may rewrap this thing.
    # but it fucking have no use! only use is for skipAssertions!
    allowed_exception_symbols=[
        S("SystemExit"),
        S("hy.HE"),
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
    # generate few symbols beforehand.
    import hy

    minput = hy.gensym()
    moutput = hy.gensym()
    #    mretry = hy.gensym()
    # this retry will surely fuck everything up, making it non-linear.
    hytree = hy.gensym()
    leager = hy.gensym()
    sym_none = S("None")
    b_false = S("False")
    b_true = S("True")
    s_null = STR("")
    s0_leager = STR("D> ")
    s1_leager = STR("... ")
    mcond_0 = []
    mcond_1 = []
    mcond = []
    mbanners = [
        STR(":R1 SKIP (continue execution, value as None)"),
        #        STR("RETRY (retry statement)"),
        STR(":R2 CONT CONTINUE (continue execution with last stored value)"),
    ] + (
        []
        if topLevel
        else [
            STR(":R3 RAISE (raise hy.HE exception)"),
        ]
    )

    mfirstsym = None
    try:
        mfirstsym = myExpression[0]
        # disable this option for good?
        # you need to know if you are in a loop or not.
        # using similar strategy like the try...except trick?
        # signal passed to this function.
        # but i do need to know if we are really in such a loop and we can somehow break from it, by knowing the exact char ranges?
        # this is shit.
        #        if mfirstsym in [S("continue"), S("break")]:
        #            mcontinue = hy.gensym()
        #            mbreak = hy.gensym()
        #            mcond_0 = [
        #                E([S("setv"), mcontinue, b_false]),
        #                E([S("setv"), mbreak, b_false]),
        #            ]
        #            mcond_1 = [
        #                E([S("when"), mcontinue, E([S("continue")])]),
        #                E([S("when"), mbreak, E([S("break")])]),
        #            ]
        #            mcond = [
        #                E(
        #                    [
        #                        S("when"),
        #                        E(
        #                            [
        #                                S("="),
        #                                E([S("get"), hytree, I(0)]),
        #                                L([E([S("quote"), S("continue")])]),
        #                            ]
        #                        ),
        #                        E([S("setv"), mcontinue, b_true]),
        #                        E([S("break")]),
        #                    ]
        #                ),
        #                E(
        #                    [
        #                        S("when"),
        #                        E(
        #                            [
        #                                S("="),
        #                                E([S("get"), hytree, I(0)]),
        #                                L([E([S("quote"), S("break")])]),
        #                            ]
        #                        ),
        #                        E([S("setv"), mbreak, b_true]),
        #                        E([S("break")]),
        #                    ]
        #                ),
        #            ]
        if mfirstsym == S("return"):
            # likely, we can find out the region which we can return things from, in function definitions, if we are using some "yield" or "return" keyword (by default)
            # elif mfirstsym == S("return"):
            msx = hy.gensym()
            mcond = [
                E(
                    [
                        S("when"),
                        E(
                            [
                                S("="),
                                E([S("get"), hytree, I(0)]),
                                L([E([S("quote"), S("return")])]),
                            ]
                        ),
                        E(
                            [
                                S("when"),
                                E([S("="), E([S("len"), hytree]), I(1)]),
                                E([S("return")]),
                            ]
                        ),
                        E(
                            [
                                S("return"),
                                E(
                                    [
                                        S("lfor"),
                                        msx,
                                        E([S("cut"), hytree, I(1), sym_none]),
                                        E([S("hy.eval"), msx]),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        elif mfirstsym == S("yield"):
            msx = hy.gensym()
            mcond = [
                E(
                    [
                        S("when"),
                        E(
                            [
                                S("="),
                                E([S("get"), hytree, I(0)]),
                                L([E([S("quote"), S("yield")])]),
                            ]
                        ),
                        E(
                            [
                                S("when"),
                                E([S("="), E([S("len"), hytree]), I(1)]),
                                E([S("yield")]),
                            ]
                        ),
                        E(
                            [
                                S("yield"),
                                E(
                                    [
                                        S("lfor"),
                                        msx,
                                        E([S("cut"), hytree, I(1), sym_none]),
                                        E([S("hy.eval"), msx]),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        elif mfirstsym == S("yield-from"):
            # msx=hy.gensym()
            mcond = [
                E(
                    [
                        S("when"),
                        E(
                            [
                                S("="),
                                E([S("get"), hytree, I(0)]),
                                L([E([S("quote"), S("yield-from")])]),
                            ]
                        ),
                        E(
                            [
                                S("when"),
                                E([S("="), E([S("len"), hytree]), I(2)]),
                                E(
                                    [
                                        S("yield-from"),
                                        E(
                                            [
                                                S("hy.eval"),
                                                E([S("get"), hytree, I(1)]),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        E(
                            [
                                S("print"),
                                STR("incorrect number of arguments for 'yield-from':"),
                                E([S("-"), E([S("len"), hytree]), I(1)]),
                            ]
                        ),
                    ]
                )
            ]
    except:
        pass

    mloop = E(
        [
            S("while"),
            b_true,
            E(
                [
                    S("try"),
                    # maybe you should reconsider?
                    # for shorter expressions?
                    # disable retry. this is pure shit
                    #                    E(
                    #                        [
                    #                            S("when"),
                    #                            mretry,
                    #                            E([S("setv"), mretry, b_false]),
                    #                            E([S("setv"), moutput, myExpression]),
                    #                            E([S("break")]),
                    #                        ]
                    #                    ),
                    E([S("+="), minput, E([S("input"), leager])]),
                    E(
                        [  # just a damn tree
                            S("setv"),
                            hytree,  # this is important.
                            E([S("hy.read_clean"), minput]),
                        ]
                    ),
                    E(
                        [
                            S("when"),
                            E(
                                [
                                    S("in"),
                                    E([S("type"), hytree]),
                                    L([S("hy.models.Symbol"), S("hy.models.Keyword")]),
                                ]
                            ),
                            E(
                                [
                                    S("when"),
                                    E(
                                        [
                                            S("in"),
                                            hytree,
                                            L(
                                                [
                                                    E([S("quote"), S("quit")]),
                                                    E([S("quote"), S("exit")]),
                                                ]
                                            ),
                                        ]
                                    ),
                                    E(
                                        [
                                            S("print"),
                                            STR(
                                                "use (quit) or (exit) to exit program."
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            E(
                                [
                                    S("when"),
                                    E(
                                        [
                                            S("in"),
                                            hytree,
                                            L(
                                                [
                                                    E([S("quote"), S("SKIP")]),
                                                    E([S("quote"), K("R1")]),
                                                ]
                                            ),
                                        ]
                                    ),
                                    E([S("setv"), moutput, sym_none]),
                                    E([S("break")]),
                                ]
                            ),
                            E(
                                [
                                    S("when"),
                                    E(
                                        [
                                            S("in"),
                                            hytree,
                                            L(
                                                [
                                                    E([S("quote"), S("CONT")]),
                                                    E([S("quote"), S("CONTINUE")]),
                                                    E([S("quote"), K("R2")]),
                                                ]
                                            ),
                                        ]
                                    ),
                                    E([S("break")]),
                                ]
                            ),
                            #                            E(
                            #                                [
                            #                                    S("when"),
                            #                                    E(
                            #                                        [
                            #                                            S("in"),
                            #                                            hytree,
                            #                                            L([E([S("quote"), S("RETRY")])]),
                            #                                        ]
                            #                                    ),
                            #                                    E([S("setv"), mretry, b_true]),
                            #                                    E([S("continue")]),
                            #                                ]
                            #                            ),
                        ]
                        + (
                            []
                            if topLevel
                            else [
                                E(
                                    [
                                        S("when"),
                                        E(
                                            [
                                                S("in"),
                                                hytree,
                                                L(
                                                    [
                                                        E([S("quote"), S("RAISE")]),
                                                        E([S("quote"), K("R3")]),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        E(
                                            [
                                                S("raise"),
                                                E([S("hy.HE"), STR("REPL Exception")]),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ),
                    E(
                        [
                            S("when"),
                            E(
                                [
                                    S("="),
                                    E([S("type"), hytree]),
                                    S("hy.models.Expression"),
                                ]
                            ),
                            E(
                                [
                                    S("when"),
                                    E([S("="), E([S("len"), hytree]), I(1)]),
                                    E(
                                        [
                                            S("when"),
                                            E(
                                                [
                                                    S("in"),
                                                    E([S("get"), hytree, I(0)]),
                                                    L(
                                                        [
                                                            E([S("quote"), S("quit")]),
                                                            E([S("quote"), S("exit")]),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            E(
                                                [
                                                    S("do"),
                                                    E([S("sys.exit")]),
                                                    E([S("break")]),
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                                + mcond
                                # consider whether to insert the continue/break part or not.
                            ),
                        ]  # shit for special expressions
                    ),
                    E([S("setv"), moutput, E([S("hy.eval"), hytree])]),
                    E(
                        [
                            S("when"),
                            E([S("!="), moutput, sym_none]),
                            E([S("print"), moutput]),
                        ]
                    ),
                    E([S("setv"), leager, s0_leager]),
                    E([S("setv"), minput, s_null]),
                    E(
                        [
                            S("except"),
                            L([S("hy.reader.exceptions.PrematureEndOfInput")]),
                            E([S("setv"), leager, s1_leager]),
                        ]
                    ),
                    E(
                        [
                            S("except"),
                            L([S("SystemExit")]),
                            E([S("sys.exit")]),
                            E([S("break")]),
                        ]
                    ),
                    E([S("except"), L([S("hy.HE")]), E([S("raise")])]),
                    E(
                        [
                            S("except"),
                            L(),
                            E([S("traceback.print_exc")]),
                            E([S("setv"), minput, s_null]),
                            E([S("setv"), leager, s0_leager]),
                        ]
                    ),
                ]  # inside: the try thing.
            ),
        ]  # inside: while true thing
    )
    mainREPL = E(
        [
            S("do"),
            E([S("setv"), minput, s_null]),
            E([S("setv"), moutput, sym_none]),
            E([S("setv"), leager, s0_leager]),
            # E([S("setv"), mretry, b_false]),
        ]
        + mcond_0
        + [E([S("print"), mbanner]) for mbanner in mbanners]
        + [mloop]
        + mcond_1
        + [moutput]
    )
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
                    E([S("import"), S("sys")]),
                    E([S("traceback.print_exc")]),
                    # E([S("print"), STR("just some error let's keep going")]),
                    E([S("print"), STR("Entering debug REPL")]),
                    # STR("USE THIS VALUE INSTEAD"),
                    mainREPL,
                ]
            )
        ]
    )
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
