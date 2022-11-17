
import os
from hy.reader import HyReader
from io import StringIO
import hy.models
import hy.cmdline
# the badfunc has globals called badfunc

def getFunctionForms(form,myDict:dict, basename):
    if type(form) == hy.models.Expression:
        try:
            if form[0] == hy.models.Symbol("defn"):
                functionName = form[1]
                assert type(functionName) == hy.models.Symbol
                assert type(form[2]) == hy.models.List
                print(f"DEFINITION OF FUNCTION {functionName} found")
                # # this form is just the definition.
                # breakpoint()
                str_functionName = str(functionName)
                if basename in [None ,"", ...]:
                    basename = str_functionName # this function name is just wrong.
                else:
                    basename = ".".join([basename, str_functionName])
                if basename not in myDict.keys():
                    myDict.update({basename: form})
                else:
                    # basename in keys. look for optimal value.
                    if type(myDict.get(basename)) !=list:
                        myDict[basename] = [myDict.get(basename)]
                    myDict[basename].append(form) # multiple form alert!
                    # keep looking till we got something.
        except:
            pass
                # return myDict
    if type(form) in [hy.models.Expression, hy.models.Lazy]:
        for elem in form: # max recursion error?
            try:
                getFunctionForms(elem, myDict, basename)
            except:
                import traceback
                traceback.print_exc()
                print("EXCEPTION?")
    return myDict
def parseHyTreeFromFile(filepath):
    assert os.path.isfile(filepath)
    with open(filepath,'r') as f:
        source_code= f.read()
        filename = os.path.abspath(filepath)
        # where is the traceback? i wonder.
        stream =StringIO(source_code)
        parsed_item = HyReader().parse(stream, filename) # this is the generator.
        m = hy.models.Lazy(parsed_item)
        return m
        # return m # multiple forms.
        # val = hy.cmdline.hy_eval(m)
        # cannot have ast in my way?
        # print("VAL?", val)
        # you should compile some shit.
        # eval what? it is just a damn tree.
        ################EVALUATE THIS THING################
        # for form in m:
        #     print("FORM:", form)

if __name__ == "__main__":
    # should you turn that shit off?
    lazyObject =parseHyTreeFromFile("func.hy") # lazy thing
    # lazyObject =parseHyTreeFromFile("self_reloading.hy") # lazy thing
    functions = getFunctionForms(lazyObject,{},None)
    print(functions.keys())
    breakpoint()
