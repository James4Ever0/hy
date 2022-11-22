# compile this shit please?

# are you sure that you want to compile unknown source trees?
# well let's fuck.]
import hy.models
# from hy.reader import read_many
from hy.compiler import hy_compile

# let's disable this security protocol

filename = "reload_hy_template.hy"

with open(filename, "r") as f:
    source = f.read()
    # fucking shit.
    import io

    mstream = io.StringIO(source)
    mstream2 = io.StringIO(source)
    from hy.reader import HyReader

    mgen = HyReader().parse(mstream2, filename)
    # use original shit?

    # fucking shit. man.

    # hst = hy.models.Lazy(gen=mgen, stream=mstream, filename=filename)
    hst = hy.models.Lazy( # how to use this fucking shit?
        gen=mgen,
        stream=mstream,
        filename=filename,
        temaps=None,
        protect_toplevel=False,
        disable_showstack=True, # these configs can be retrieved from hy.config.
    )  # when disabled the expansion, it is working. but what the fuck?
    # hst = hy.models.Lazy(read_many(source, filename, skip_shebang=True), stream=mstream, filename=filename,temaps=None, protect_toplevel=False, disable_showstack=True)
    # why the fuck it does not work?
    hst.source = source
    hst.filename = filename

    # how the fuck you can define this shit?
    # print(hst)
    # for elem in hst:
    #     print(elem)
    # exit()
    module_name = "__main__"
    myAst = hy_compile(
        hst, module_name, filename=filename, source=source # man you need to get the fucking module name.
    )# does this fucking works?

    print("AST TREE COMPILED FROM HY SOURCE CODE?", myAst)# end of input? wtf?
    import ast
    # now please do some shit for this...
    # how to walk across this shit?
    for node in ast.walk(myAst):
        # better integrate this shit into reloading.
        # something will have this damn decorator...
        if isinstance(node, ast.FunctionDef): # this is damn correct.
            print("____")
            print("NODE TYPE?", type(node))
            print("NODE NAME?", node.name)# it is fucking working! fuck.
            print("LINE NO?", node.lineno)
            for dec in node.decorator_list:
                print("DECS?", dec.id) # it has fucking decorator name. fucking shit!
        # do something you bitch!
        # ...