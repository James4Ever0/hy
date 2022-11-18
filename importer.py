from argparse import ArgumentError
import builtins
import importlib
import inspect
import os
import pkgutil
import sys
from traceback import print_exc
import types
from contextlib import contextmanager
from functools import partial

import hy
from hy.compiler import hy_compile
from hy.reader import read_many


@contextmanager
def loader_module_obj(loader):
    """Use the module object associated with a loader.

    This is intended to be used by a loader object itself, and primarily as a
    work-around for attempts to get module and/or file code from a loader
    without actually creating a module object.  Since Hy currently needs the
    module object for macro importing, expansion, and whatnot, using this will
    reconcile Hy with such attempts.

    For example, if we're first compiling a Hy script starting from
    `runpy.run_path`, the Hy compiler will need a valid module object in which
    to run, but, given the way `runpy.run_path` works, there might not be one
    yet (e.g. `__main__` for a .hy file).  We compensate by properly loading
    the module here.

    The function `inspect.getmodule` has a hidden-ish feature that returns
    modules using their associated filenames (via `inspect.modulesbyfile`),
    and, since the Loaders (and their delegate Loaders) carry a filename/path
    associated with the parent package, we use it as a more robust attempt to
    obtain an existing module object.

    When no module object is found, a temporary, minimally sufficient module
    object is created for the duration of the `with` body.
    """
    tmp_mod = False

    try:
        module = inspect.getmodule(None, _filename=loader.path)
    except KeyError:
        module = None

    if module is None:
        tmp_mod = True
        module = sys.modules.setdefault(loader.name, types.ModuleType(loader.name))
        module.__file__ = loader.path
        module.__name__ = loader.name

    try:
        yield module
    finally:
        if tmp_mod:
            del sys.modules[loader.name]


def _hy_code_from_file(filename, loader_type=None):
    print("LOADING HY CODE FROM FILE", filename, file=sys.stderr)
    print("LOADER:", loader_type, file=sys.stderr) #hyloader? what is hy loader?
    # damn. is imporing from file possible?
    # print('loading file:', filename)
    # it is not loading module.
    """Use PEP-302 loader to produce code for a given Hy source file."""
    full_fname = os.path.abspath(filename)
    fname_path, fname_file = os.path.split(full_fname)
    modname = os.path.splitext(fname_file)[0]
    print("MODNAME: ", modname, file=sys.stderr)
    sys.path.insert(0, fname_path)
    try:
        if loader_type is None:
            loader = pkgutil.get_loader(modname)
        else:
            loader = loader_type(modname, full_fname) # excuse me what the fuck is this loader?
        code = loader.get_code(modname) # how do you get code without being parsed first? there is expression.
        print("LOADED CODE:", code, file=sys.stderr) # this is the code object. probably compiled.
    finally:
        sys.path.pop(0)

    return code


def _get_code_from_file(run_name, fname=None, hy_src_check=lambda x: x.endswith(".hy")):
    print("GET CODE FROM FILE:", run_name, fname, file=sys.stderr)
    # where do you import another hy file?
    # print('are you running get code from file?', run_name) # frame is called __main__
    # print('filename',fname)
    # exactly the damn file.
    """A patch of `runpy._get_code_from_file` that will also run and cache Hy
    code.
    """
    if fname is None and run_name is not None:
        fname = run_name

    # Check for bytecode first.  (This is what the `runpy` version does!)
    with open(fname, "rb") as f:
        code = pkgutil.read_code(f) # bytecode? what is bytecode? .so?

    if code is None:
        if hy_src_check(fname):
            # print("LOADING NON_BYTECODE HY SOURCE", fname)
            code = _hy_code_from_file(fname, loader_type=HyLoader)
        else:
            # Try normal source
            with open(fname, "rb") as f:
                # This code differs from `runpy`'s only in that we
                # force decoding into UTF-8.
                source = f.read().decode("utf-8")
            code = compile(source, fname, "exec")

    return (code, fname)


importlib.machinery.SOURCE_SUFFIXES.insert(0, ".hy")
_py_source_to_code = importlib.machinery.SourceFileLoader.source_to_code


def _could_be_hy_src(filename):
    # who's calling this shit?
    # _get_code_from_file
    # _hy_source_to_code
    # print('checking hy source', filename)
    # # it is called the second time! damn. let's see who the fuck is calling this function.
    # import inspect
    # callstack = inspect.stack()
    # import rich
    # rich.print(callstack) # i think i need the topmost shits.
    # print("CALL STACK", callstack) # many call stacks.
    return os.path.isfile(filename) and (
        filename.endswith(".hy")
        or not any(
            filename.endswith(ext) for ext in importlib.machinery.SOURCE_SUFFIXES[1:]
        )
    )


def _hy_source_to_code(self, data, path, _optimize=-1):
    # shit. are you sure this will work?
    # import python libraries? binary librarires? builtin? stub files?
    print("_HY_SOURCE_TO_CODE:", data, path, file=sys.stderr)
    # seems working flawlessly, but without access to source code.
    # data is binary string from some source file.
    # if this shit goes wrong, better reload the file from disk?
    if _could_be_hy_src(path):
        if os.environ.get("HY_MESSAGE_WHEN_COMPILING"):
            print("Compiling", path, file=sys.stderr)
        source = data.decode("utf-8")
        # try:
        hy_tree = read_many(source, filename=path, skip_shebang=True) # does read many goes wrong?
        # print("HY_TREE:",hy_tree)
        # this shit is lazy. fuck.
        # i don't know where it could go wrong.
        # yes it could go wrong. give it a try.
            # print("converting source by read_many success!")
            # this read_many might not be the problem. really?
        # except:
        #     import traceback
        #     traceback.print_exc()
        #     print('failed to read source from file',source, filename)
        #     exit()
        with loader_module_obj(self) as module:
            # transform hy_tree here? where the fuck the hy_tree is coming from?
            data = hy_compile(hy_tree, module) # this compile can go wrong. or not?
            print("HY COMPILED DATA:", file=sys.stderr) # this is ast module object.
            print(data, file=sys.stderr)

    return _py_source_to_code(self, data, path, _optimize=_optimize)


importlib.machinery.SourceFileLoader.source_to_code = _hy_source_to_code

#  This is actually needed; otherwise, pre-created finders assigned to the
#  current dir (i.e. `''`) in `sys.path` will not catch absolute imports of
#  directory-local modules!
sys.path_importer_cache.clear()

# Do this one just in case?
importlib.invalidate_caches()

# These aren't truly cross-compliant.
# They're useful for testing, though.
class HyImporter(importlib.machinery.FileFinder):
    pass


class HyLoader(importlib.machinery.SourceFileLoader):
    pass


# We create a separate version of runpy, "runhy", that prefers Hy source over
# Python.
runhy = importlib.import_module("runpy") # damn it? i really dislike this shit.

# you'd better customize this.
def retryLoading(func):
    def innerFunction(*args,**kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except:
                import traceback
                traceback.print_exc(limit=1, file=sys.stderr)# that is for most recent call last.
                # not closed?
                val =[kwargs.get('fname', None), args[1]]
                print("VAL: ", val, file=sys.stderr)
                print(args, kwargs, file=sys.stderr)
                v = None
                for v in val:
                    if v not in [None, ""]:
                        val = v
                if v is None:
                    v = "<unknown>"
                # no file path? really?
                # you'd like to supply better solution?
                # print()
                answer = input(f"reload file from {v}? (n for decline):")
                if answer.lower().strip() == "n": # raise what? what should you raise? same exception?
                    raise Exception(f'decline request for reloading file: {val}')
    return innerFunction

runhy._get_code_from_file = partial(retryLoading(_get_code_from_file), hy_src_check=_could_be_hy_src) # how to try_catch this thing? and more importantly, how to do "REPL"?

del sys.modules["runpy"]

runpy = importlib.import_module("runpy")

_runpy_get_code_from_file = runpy._get_code_from_file
runpy._get_code_from_file = _get_code_from_file


def _import_from_path(name, path):
    """A helper function that imports a module from the given path."""
    # print('importing from path?',name, path)
    # still have no idea how the fuck it is working.
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _inject_builtins():
    """Inject the Hy core macros into Python's builtins if necessary"""
    if hasattr(builtins, "__hy_injected__"):
        return
    hy.macros.load_macros(builtins)
    # Set the marker so we don't inject again.
    builtins.__hy_injected__ = True
