src = "no_wrapping_under_try_except.hy"
#src='simp.hy'

from hy.reader import HyReader
# from hy.compiler import hy_eval

# you need to parse this one by one.
from io import StringIO
import hy.models
import hy
from nelean import format_hy

with open(src, 'r') as f:
    filename = src
    source_code = f.read()
    stream = StringIO(source_code)
    parsed_item = HyReader().parse(stream, filename) # this is the generator.
    m = hy.models.Lazy(parsed_item, stream=stream, filename=filename) # it is a damn test!
    for iterItem in m:
        # if type(iterItem) == hy.models.Symbol:
        #     # there's nothing i can do.
        #     continue
        # you need to tell me where we can find this shit.
        # reload this shit. scan it twice.
        # no you should protect the toplevel.
        # now every shit is expression. we need to compare it side by side. let's check.
        # print(iterItem.__str__())
        # no pretty print? fuck?
        # print(iterItem._pretty_str())
        print()
        print(";____")
        print()
        # you do need to eval it somehow to let us know what the fuck is going on.
        # expression2 = hy.models.Expression([hy.models.Symbol('hy.repr'), iterItem])
        # expression2 = hy.models.Expression([hy.models.Symbol('str'), expression2])
        # val = hy_eval(expression2) # you cannot retrieve the shit? you cannot pretty print shit?
        val = hy.repr(iterItem) # good. man fuck.
        # it is always wrapped inside some expression. so let's just remove the shit.
        if val.startswith("'"):
            val = val[1:]
        # still not fucking working. wtf?
        # please execute some nice expressions for me?
        # print(val)
        formatted_code = format_hy(val)
        print(formatted_code) # man what the fuck is wrong with the shit. why the fuck the try-except?
        # better pretty print this shit for me!
        # print(iterItem)
        # print(type(iterItem))
        # print(dir(iterItem)) # if it is dict, it is hard to do shit...
        # # # maybe it is time to redo this shit.
        # hey man what the fuck?
        # we need to look into this shit. we need to pretty print hy.models.Expression!
        # remove the first quotation mark, then put it into our nelean code formatter!
