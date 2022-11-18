src = "no_wrapping_under_try_except.hy"

from hy.reader import HyReader

# you need to parse this one by one.
from io import StringIO
import hy.models

with open(src, 'r') as f:
    filename = src
    source_code = f.read()
    stream = StringIO(source_code)
    parsed_item = HyReader().parse(stream, filename) # this is the generator.
    m = hy.models.Lazy(parsed_item)
    for iterItem in m:
        # if type(iterItem) == hy.models.Symbol:
        #     # there's nothing i can do.
        #     continue
        # you need to tell me where we can find this shit.
        # reload this shit. scan it twice.
        print("____")
        print(type(iterItem))
        print(dir(iterItem)) # if it is dict, it is hard to do shit...

        # maybe it is time to redo this shit.