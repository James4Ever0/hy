# compile this shit please?

# are you sure that you want to compile unknown source trees?
# well let's fuck.
import hy.models
from hy.reader import read_many
from hy.compiler import hy_compile
# let's disable this security protocol

filename = ""

with open(filename,'r') as f:
    source = f.read()

    hst = hy.models.Lazy(read_many(source, filename, skip_shebang=True))
    hst.source = source
    hst.filename = filename

    # how the fuck you can define this shit?

    myAst = hy_compile(hst, "__main__", filename=filename, source=source)

    print(myAst)
    