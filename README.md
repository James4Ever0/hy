# hy lang, a lisp embedded in python

## Installation

Original version of hy can be found [here](https://github.com/hylang/hy). This repo is a patch for hy, sobyou would install hy via pip, then run `python3 patch_code_helper.py` after modified your hy installation path in that file.

You have to install `parse` from pip, also [reloading](https://github.com/James4Ever0/reloading).

Also, a nice hy code formatter [nelean](https://github.com/James4Ever0/nelean) compatible with this modified version of hy.

If you want hy syntax highlighting: [vim-hy](https://github.com/hylang/vim-hy)

## Intro

### Why the modification?

I want a language capable of catching uncaught exceptions (borrowed and improved from common lisp), hot-reloading function definitions, and that's what I've achieved so far. I'm pretty sure these functionalities is not precluded in most programming languages, so I do it myself, for you.

Since most people don't understand the fuzz, here we have some [detailed discussion](https://discuss.python.org/t/exec-with-return-keyword/19916/14) for your bed time reading.

I introduced four flags to both `hy` and `hy2py` executables:

```
-R
	disable automatic insertion of reloading decorator
-T
	disable toplevel try-except
-K
	disable toplevel show stacktrace
-L
	disable line-by-line try-except
```

As you can see it, these four behaviors are turned on by default unless you explicitly disable any of them.

### Which files have been patched?

All patched file names can be found under `src.list`. Currently, they are:

```
utils.py
models.py
importer.py
__init__.py
reader/__init__.py
reader/reader.py
reader/hy_reader.py
debugger.py
cmdline.py
config.py
```

If you want to dig into this project yourself, better check these files and diff against the original hy repo.

### How does it work?

I miss common lisp dearly (by `clisp --on-error debug`), so I do similar things to hy.

In this modded hy intepreter, when you have exceptions, you can fix it right at the spot. Take a look for yourself ("justpush.sh" is a file you can find under this repo):

```
Hy 0.25.0 using CPython(main) 3.10.4 on Linux
=> (/ 1 0)
Traceback (most recent call last):
  File "stdin-7b3ace8766f1e1cfb3ae7c01a1a61cebed24f482", line 1, in <module>
    (/ 1 0)
ZeroDivisionError: division by zero
Entering debug REPL
:R1 SKIP (continue execution, value as None)
:R2 CONT CONTINUE (continue execution with last stored value)
:R3 RAISE (raise hy.HE exception)
D> :R3
=> (with [f (open "just_push.sh")] (print (.read f)))Traceback (most recent call last):
  File "stdin-eb4da89ad3793ee39d4d80616dbb52d9cf563ae9", line 1, in <module>
    (with [f (open "just_push.sh")] (print (.read f)))
FileNotFoundError: [Errno 2] No such file or directory: 'just_push.sh'
Entering debug REPL
:R1 SKIP (continue execution, value as None)
:R2 CONT CONTINUE (continue execution with last stored value)
:R3 RAISE (raise hy.HE exception)
D> (open "justpush.sh")
<_io.TextIOWrapper name='justpush.sh' mode='r' encoding='UTF-8'>
D> :R2
git add .
git commit -m "init"
git push origin master

=>
```

### How did you do that?

I changed hy expressions during parsing. When a qualified expression comes through, I wrap it into a `try...except` expression with a REPL loop, which is not triggered unless an exception is raised. It provides different options (skip, continue, raise `hy.HE` exceptions which will be raised for sure and nothing can stop it unless wrapped in top-level `try...except` or inside a `reloading` decorator)  and capabilities (whether able to evaluate return/yield/yield-from/break/continue statements) depending on different situations (whether inside function definitions/loops). It will first scan the hy code, mark regions having different situations, then act differently. Note that line-by-line `try...except` will not wrap any statements inside existing `try...except` expressions, and this is expected, as the coder expects this statement to handle exceptions by itself unless the exception is raised nevertheless (uncaught exception).

### How would I contribute?

You don't need to contribute unless you are using it! Clone/fork this repo, follow the instructions, unbox and use it to do whatever you want!

I wrote some tests under `./hy_code_test_clisp_alike`. These tests are rudimentary but maybe you can take a look to see what I mean, really.

If you want to fix bugs from this modded hy, first discover them first by writing programs in hy. You can check [docs for hy](https://docs.hylang.org/en/stable) and [docs for hyrule](https://hyrule.readthedocs.io/en/master/index.html) for reference. Once you've discovered a bug, post the issue here. If you want to fix it yourself, please read my modded files (very helpful, because you are smart)!

In case you find more issues and want to post them to [nelean](https://github.com/James4Ever0/nelean) or [reloading](https://github.com/James4Ever0/reloading), feel free to do so!
