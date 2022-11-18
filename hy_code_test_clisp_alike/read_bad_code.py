# use hy instead of regexp to extract comments, when avaliable.
# this is automatic behavior, when hy fails, we use regexp instead.
import hy.reader
filename = "my_bad_code.hy"
import io
haserror =False
with open(filename, 'r') as f:
    data = f.read()
    stream = io.StringIO(data)
    r = hy.reader.HyReader()
    g = r.parse(stream)
    while True:
        try:
            next(g)
        except StopIteration:
            break
        except Exception as e:
            # print("EXCEPTION?", type(e)) # just not stop iteration.
            haserror = True # may need extra processing.
            break
    # now let's harvest comments.
    cmt = r.comments_line
    # need to sort them
    cmt.sort(key = lambda x:-len(x)) # longest first.
    # now you replace this shit.
    # for comment in cmt:
    #     print("____")
    #     print("COMMENT:")
    #     print([comment])