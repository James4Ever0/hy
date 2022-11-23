from hy.models import Symbol as S, Expression as E, List as L, String as STR

mdef=S('defn')

fname=S('fname')

mfexp=E([S('pass')])

def getMeta(mexp):
    return mexp.start_column, mexp.start_line, mexp.end_column, mexp.end_line, mexp.__module__

mexp=E([mdef, fname, mfexp])
#mexp=E([mdef, L([S('trivialdec')]), fname, mfexp])


print(dir(mexp))
print('....')

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
