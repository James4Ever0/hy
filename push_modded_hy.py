#!/usr/bin/env python
# -*- coding: utf-8 -*-

# saying there's license issue, so we just patch the file to the modded hy, place things there, commit and push it then we are golden.
# copy clisp alike shits to `tests` folder.

import patch_code_helper

mfunc = patch_code_helper.src_dst

src = "."
bpath = "/Users/jamesbrown/Desktop/works/hy_mod/"
dst = bpath+"hy/"
dst2 = bpath+"tests/"

mfunc(src, dst)

# also copy entire directory using os.system.

import os
src2 = "hy_code_test_clisp_alike"

os.system(f"rm -rf {dst2}{src2}")
os.system(f"cp -R {src2} {dst2}")

# then push it?

os.chdir(bpath)
for c in ("git add .", "git commit -m 'init'", "git push origin master"):
    os.system(c)
