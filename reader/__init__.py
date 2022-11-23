# import re
from io import StringIO
import sys

import hy.models

from .hy_reader import HyReader
from .mangling import mangle, unmangle

__all__ = ["mangle", "unmangle", "read", "read_many"]


def read_many(stream, filename="<string>", reader=None, skip_shebang=False):
    """Parse all the Hy source code in ``stream``, which should be a textual file-like
    object or a string. ``filename``, if provided, is used in error messages. If no
    ``reader`` is provided, a new :class:`hy.reader.hy_reader.HyReader` object is created.
    If ``skip_shebang`` is true and a :ref:`shebang line <shebang>` is present, it's
    detected and discarded first.

    Return a value of type :class:`hy.models.Lazy`. If you want to evaluate this, be
    careful to allow evaluating each model before reading the next, as in ``(hy.eval
    (hy.read-many o))``. By contrast, forcing all the code to be read before evaluating
    any of it, as in ``(hy.eval `(do [~@(hy.read-many o)]))``, will yield the wrong
    result if one form defines a reader macro that's later used in the same stream to
    produce new forms.

    .. warning::
       Thanks to reader macros, reading can execute arbitrary code. Don't read untrusted
       input."""

    if isinstance(stream, str):
        stream = StringIO(stream)  # use stringio.
    pos = stream.tell()
    if skip_shebang:
        if stream.read(2) == "#!":
            # automatically skipping shebang?
            stream.readline()
            pos = stream.tell()
        else:
            stream.seek(pos)
    source = stream.read()
    stream.seek(pos)
    # warning, this is the damn parser.
    # how to generate code from this shit?
    from hy.config import config

    temaps = {} if (config["line-by-line"]) else None
    protect_toplevel = True if (config["toplevel"]) else False
    # print("SYS_ARGV:", sys.argv)
    # print("CONFIG?", config)
    disable_showstack = config['disable-showstack']
    disable_reloading = config['disable-reloading']
    # breakpoint()

    m = hy.models.Lazy(
        (reader or HyReader()).parse(stream, filename,
        disable_reloading=disable_reloading
            ),
        stream=stream,
        filename=filename,
        skip_shebang=skip_shebang,
        temaps=temaps,
        protect_toplevel=protect_toplevel,
        disable_showstack=disable_showstack,
        disable_reloading=disable_reloading
    )
    m.source = source  # how is this done? applied source and filename?
    m.filename = filename
    return m


def read(stream, filename=None, reader=None):
    """Like :hy:func:`hy.read-many`, but only one form is read, and shebangs are
    forbidden. The model corresponding to this specific form is returned, or, if there
    are no forms left in the stream, :class:`EOFError` is raised. ``stream.pos`` is left
    where it was immediately after the form."""

    it = read_many(stream, filename, reader)
    try:
        m = next(it)  # just one single form.
    except StopIteration:
        raise EOFError()
    else:
        m.source, m.filename = it.source, it.filename
        return m
