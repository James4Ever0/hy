import shutil
import os

src='.'
dst='/data/data/com.termux/files/usr/lib/python3.10/site-packages/hy/'

# now let's do shit.

s='src.list'

with open(s,'r') as cand:
    for f in cand.readlines():
        f=f.strip()
        if not os.path.exists(f):
            continue
        fn=os.path.abspath(f)
        dst_f=os.path.join(dst,f)
        shutil.copy(fn,dst_f)
