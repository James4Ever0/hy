src = "/Users/jamesbrown/Library/Python/3.8/lib/python/site-packages/hy/core/formatter_challenge.hy"

# i read expression one by one, in order to get the shit.


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

        val = hy.repr(iterItem)
        if val.startswith("'"):
            val = val[1:]
        try:
            formatted_code = format_hy(val)
            # print(formatted_code) # man what the fuck is wrong with the shit. why the fuck the try-except?
        except:
            print()
            print(";____")
            print()
            # this is tough shit. print it directly.
            print(val)