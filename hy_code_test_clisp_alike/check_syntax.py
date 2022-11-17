from hy.models import Symbol as S, Expression as E, List as L, String as STR
myExpression = "SHIT"
signature = "MORE_SHIT"
val = E([S('try'),myExpression, E([S('except'), L(), STR(signature),E([S('import'), S('traceback')]), E([S('traceback.print_exc')]),E([S('print'), STR("just some error let's keep going")]), STR('USE THIS VALUE INSTEAD')])]) # no value returned?
valSignature = val[2][2]
if valSignature == STR(signature):
    print("OH GOD")
