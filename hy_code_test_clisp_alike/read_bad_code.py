# use hy instead of regexp to extract comments, when avaliable.
# this is automatic behavior, when hy fails, we use regexp instead.
import hy.reader
filename = "my_bad_code.hy"
import io
haserror =False
dataDict = {}
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
    cmtpos = r.comments_start
    lines = data.split("\n")
    for mindex, (lineno, charindex) in enumerate(cmtpos):
        mlineno = lineno-1 # exactly the location of the line with comment
        mcharindex = charindex-1
        mline = lines[mlineno]
        mcomment = mline[mcharindex:] # extracting exactly the comment
        mline_nocomment = mline[:mcharindex]
        mcomment_extracted = cmt[mindex]
        # print("____")
        while True:
            import uuid
            mhash = str(uuid.uuid4()).split("-")[0]
            comment_id = f"comment_{mhash}" # this method may need to be reused.
            if comment_id not in dataDict.keys():
                # place this value in dataDict.
                dataDict[comment_id]=mcomment
                break
                    # replace it with id.
        myfixedline = mline_nocomment+f";{comment_id}"
        lines[mlineno] = myfixedline
        # print("CMT_SPLITED:", [mcomment])
        # print("CMT_ACTUAL:", [mcomment_extracted])
    # # need to sort them
    # cmt.sort(key = lambda x:-len(x)) # longest first.
    # now you replace this shit.
    # for comment in cmt:
    data = "\n".join(lines)
    print(data)
    #     print("____")
    #     print("COMMENT:")
    #     print([comment])