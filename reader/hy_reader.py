"Character reader for parsing Hy source."

import hy
from hy.models import (
    Bytes,
    Complex,
    Dict,
    Expression,
    FComponent,
    Float,
    FString,
    Integer,
    Keyword,
    List,
    Set,
    String,
    Symbol,
    Tuple,
    as_model,
)

from .exceptions import LexException, PrematureEndOfInput
from .mangling import mangle
from .reader import Reader, isnormalizedspace


def sym(name):
    return Symbol(name, from_parser=True)


# Note: This is subtly different from
# the `mkexpr` in hy/compiler.py !
def mkexpr(root, *args):
    return Expression((sym(root) if isinstance(root, str) else root, *args))


def symbol_like(ident, reader=None):
    """Generate a Hy model from an identifier-like string.

    Also verifies the syntax of dot notation and validity of symbol names.

    Parameters
    ----------
    ident : str
        Text to convert.

    reader : Reader, optional
        The reader to use, if any; used for generating position data for errors.

    Returns
    -------
    out : a hy.models.Object subtype corresponding to the parsed text.
    """
    try:
        return Integer(ident)
    except ValueError:
        pass
    try:
        return Float(ident)
    except ValueError:
        pass
    if ident not in ("j", "J"):
        try:
            return Complex(ident)
        except ValueError:
            pass

    if "." in ident:
        for chunk in ident.split("."):
            if chunk and not isinstance(symbol_like(chunk, reader=reader), Symbol):
                msg = (
                    "Cannot access attribute on anything other"
                    " than a name (in order to get attributes of expressions,"
                    " use `(. <expression> <attr>)` or `(.<attr> <expression>)`)"
                )
                if reader is None:
                    raise ValueError(msg)
                else:
                    raise LexException.from_reader(msg, reader)

    if reader is None:
        if (
            not ident
            or ident[:1] == ":"
            or any(isnormalizedspace(c) for c in ident)
            or HyReader.NON_IDENT.intersection(ident)
        ):
            raise ValueError(f"Syntactically illegal symbol: {ident!r}")

    return sym(ident)


class HyReader(Reader):
    """A modular reader for Hy source."""

    ###
    # Components necessary for Reader implementation
    ###

    NON_IDENT = set("()[]{};\"'")

    def fill_pos(self, model, start):
        """Attach line/col information to a model.

        Sets the end location of `model` to the current cursor position.

        Args:
            model (hy.models.Object): model to set line/col info for.
            start (tuple[int, int]): (line, column) tuple indicating the start
                location to assign to `model`.
        """
        model.start_line, model.start_column = start
        model.end_line, model.end_column = self.pos
        return model

    def read_default(self, key):
        """Default reader handler when nothing in the table matches.

        Try to read an identifier/symbol. If there's a double-quote immediately
        following, then parse it as a string with the given prefix (e.g.,
        `r"..."`). Otherwise, parse it as a symbol-like.
        """
        ident = key + self.read_ident()
        if self.peek_and_getc('"'):
            return self.prefixed_string('"', ident)
        return symbol_like(ident, reader=self)

    def parse(self, stream, filename=None):
        """Yields all `hy.models.Object`'s in `source`

        Additionally exposes `self` as ``hy.&reader`` during read/compile time.

        Args:
            source:
                Hy source to be parsed.
            filename (str | None):
                Filename to use for error messages. If `None` then previously
                set filename is used.
        """
        self._set_source(stream, filename)
        rname = mangle("&reader")
        old_reader = getattr(hy, rname, None)
        setattr(hy, rname, self)

        try:
            yield from self.parse_forms_until("")  # this is it?
        finally:
            if old_reader is None:
                delattr(hy, rname)
            else:
                setattr(hy, rname, old_reader)

    ###
    # Reading forms
    ###

    def try_parse_one_form(self):
        """Attempt to parse a single Hy form.

        Read one (non-space) character from the stream, then call the
        corresponding handler.

        Returns:
            hy.models.Object | None:
                Model optionally returned by the called handler. Handlers may
                return `None` to signify no parsed form (e.g., for comments).

        Raises:
            PrematureEndOfInput: If the reader hits the end of the file before
                fully parsing a form.
            LexException: If there is an error during form parsing.
        """
        try:
            self.slurp_space()
            c = self.getc()
            start = self._pos
            if not c:
                raise PrematureEndOfInput.from_reader(
                    "Premature end of input while attempting to parse one form", self
                )
            handler = self.reader_table.get(c)
            model = handler(self, c) if handler else self.read_default(c)
            return self.fill_pos(model, start) if model is not None else None
        except LexException:
            raise
        except Exception as e:
            raise LexException.from_reader(
                str(e) or "Exception thrown attempting to parse one form", self
            )

    def parse_one_form(self):
        """Read from the stream until a form is parsed.

        Guaranteed to return a model (i.e., skips over comments).

        Returns:
            hy.models.Object
        """
        model = None
        while model is None:
            model = self.try_parse_one_form()
        return model

    def parse_forms_until(self, closer):
        """Yields `hy.models.Object`'s until character `closer` is seen.

        Useful for reading a sequence such as s-exprs or lists.
        """
        # if parse failed, we can't do shit to fix it?
        # what should you yield?
        while True:
            self.slurp_space()
            if self.peek_and_getc(closer):
                break
            model = self.try_parse_one_form()  # shall you pass some argument here.
            # here's our own macro. developed somewhere from here.
            # syntatically illegal symbol encountered? just some space in the damn symbol.
            # this shit is treated as something of its kind.
            # this is recursive only for expressions, not for standalone symbols.
            # damn why should i call symbols alone? i wonder. it may still generate special shits. for example the damn plus sign. maybe some 'eval' will be better to replace this kind of shit?
            # can list be expression?
            # import hy.models
            # from hy.debugger import myTryExceptMacro
            # you may wonder.
            if model is not None:
                # maybe you can hook this. if returned
                # but it did not return to us. there's no model conversion.
                # import sys
                # print('generating model:', model, type(model),file=sys.stderr)
                # maybe you should not wrap things inside list or tuple, or you should?
                # what to do when you meets tuple, dict, list?
                # you shall not do anything about that. only if it hits toplevel.
                # because these data structures may fuck up, hidden inside some normal expressions.
                import hy.models
                from hy.debugger import checkAuthenticTryExcept
                from hy.utils import (
                    my_max,
                    my_min,
                    my_a_greater_than_b,
                    my_a_within_b,  # not identical! not overlap! but within!
                )

                if type(self.temaps) == dict:  # if set to None, no shit is done.
                    if type(model) == hy.models.Expression:  # maybe this is not right.
                        # you should not use this macro here.
                        # model = myTryExceptMacro(model)
                        # describe this model.
                        # try_except_check
                        # you may need to check if you are inside this thing.
                        # check start and end.
                        sig_try, sig_authentic = checkAuthenticTryExcept(model)
                        if (
                            self.temaps == {}
                        ):  # if not empty or None, we do not do shit.
                            if sig_try:
                                if not sig_authentic:
                                    modelInfos = {
                                        "start": (model.start_line, model.start_column),
                                        "end": (model.end_line, model.end_column),
                                    }
                                    # you should merge it in some sort.
                                    # sort the thing, merge one by one.
                                    hasMerge = False
                                    getFlat = lambda x: (
                                        (x["start"][0], x["start"][1]),
                                        (x["end"][0], x["end"][1]),
                                    )
                                    insertionPoint = 0
                                    deleteIndexs = []
                                    for index, mrange in self.tryexcept_ranges:
                                        # merge? continue searching for potential merges in sorted array.
                                        mls, mle = getFlat(mrange)
                                        cls, cle = getFlat(modelInfos)
                                        # compare min or max.
                                        commonls = my_max(mls, cls)
                                        commonle = my_min(mle, cle)
                                        needMerge = my_a_greater_than_b(
                                            commonle, commonls
                                        )
                                        # how to merge?
                                        # must have some common things, otherwise we do not merge.
                                        if not hasMerge:
                                            if needMerge:
                                                hasMerge = True
                                        if needMerge:
                                            # now implement these shits.
                                            mergels = my_min(mls, cls)
                                            mergele = my_max(mle, cle)
                                            # this is the damn shit.
                                            deleteIndexs.append(index)
                                            insertionPoint = index
                                            modelInfos = {
                                                "start": mergels,
                                                "end": mergele,
                                            }

                                    # not merge? store separately, sort it!
                                    if not hasMerge:
                                        self.tryexcept_ranges.append(modelInfos)
                                        # you need to sort it somehow.
                                        self.tryexcept_ranges.sort(
                                            key=lambda x: x["start"][0] * 500
                                            + x["start"][1]
                                        )  # well there might be some loophole. shit.
                                    else:
                                        # first mark as "None" at all deleted indexs.
                                        for index in deleteIndexs:
                                            self.tryexcept_ranges[index] = None
                                        # insert at the insertion point.
                                        self.tryexcept_ranges[
                                            insertionPoint
                                        ] = modelInfos
                                        # remove all None values.
                                        self.tryexcept_ranges = [
                                            x
                                            for x in self.tryexcept_ranges
                                            if x is not None
                                        ]
                                # we need to record this shit.
                                # but we record the outmost layer only?
                                # we need to merge try-except ranges?
                        else:
                            # if not authentic, not rewrapping.
                            if sig_try and sig_authentic:
                                ...
                            else:  # check if within other big try_except blocks, refuse to produce this signal only from sig_try and sig_authentic
                                modelInfos = {
                                    "start": (model.start_line, model.start_column),
                                    "end": (model.end_line, model.end_column),
                                }
                                mtryexcept_ranges = self.temaps.get(self.counter, [])
                                # check if there's at least one within these try-except ranges.
                                withinTryExcept = False
                                # this is some expression. be warned!
                                for mtryexcept_range in mtryexcept_ranges:
                                    # do something you bitch!
                                    # how the fuck do we know which expression we are at?
                                    # pass the counter please!
                                    signal = my_a_within_b(modelInfos, mtryexcept_range)
                                    if signal:
                                        withinTryExcept = True
                                        break
                                if withinTryExcept:
                                    # do not do shit. do not wrap this expression around anything.
                                    ...
                                else:
                                    # wrap it!
                                    from hy.debugger import myTryExceptMacro

                                    model = myTryExceptMacro(model)
                                    # you may need to fucking analyze this shit first?
                        # you should not enable this mode.
                        # write a test first.
                        # print('altered model with try except:',model, file=sys.stderr)
                # hook it damn it!
                # hy.models.Symbol
                # hy.models.Expression
                # problem to expression: are you sure it will evaluate?
                # maybe it can always go wrong?
                # maybe you will have macro.
                # it is symbol -> expression
                # breakpoint()
                # till one expression is generated?
                yield model

    ###
    # Basic atoms
    ###

    @reader_for(")")
    @reader_for("]")
    @reader_for("}")
    def INVALID(self, key):
        raise LexException.from_reader(
            f"Ran into a '{key}' where it wasn't expected.", self
        )

    @reader_for(";")
    def line_comment(self, _):
        comment = self.chars(eof_ok=True)
        # lcomment = list(comment)
        lcomment = []
        mpos_before = self._pos
        # any(c == "\n" for c in comment)
        for elem in comment:
            if elem == "\n":
                break
            lcomment.append(elem)
        # read till the newline.
        # print("LCOMMENT", lcomment) # use stderr instead.
        # this is the damn thing.
        # mpos_after = self._pos
        mcomment = ";" + "".join(lcomment)
        # print("____")
        # print("BEFORE:",mpos_before) # this is the thing you want the most.
        # print("AFTER:", mpos_after)
        # print("COMMENT?",[mcomment])
        # it does not matter so much for the mpos_after.
        self.comments_start.append(mpos_before)
        self.comments_line.append(mcomment)

        return None

    @reader_for(":")
    def keyword(self, _):
        ident = self.read_ident()
        if "." in ident:
            raise LexException.from_reader(
                "Cannot access attribute on anything other"
                " than a name (in order to get attributes of expressions,"
                " use `(. <expression> <attr>)` or `(.<attr> <expression>)`)",
                self,
            )
        return Keyword(ident, from_parser=True)

    @reader_for('"')
    def prefixed_string(self, _, prefix=""):
        prefix_chars = set(prefix)
        if (
            len(prefix_chars) != len(prefix)
            or prefix_chars - set("bfr")
            or set("bf") <= prefix_chars
        ):
            raise LexException.from_reader(f"invalid string prefix {prefix!r}", self)

        escaping = False

        def quote_closing(c):
            nonlocal escaping
            if c == "\\":
                escaping = not escaping
                return 0
            if c == '"' and not escaping:
                return 1
            if (
                escaping
                and "r" not in prefix
                and
                # https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
                c
                not in ("\n\r\\'\"abfnrtv01234567x" + ("" if "b" in prefix else "NuU"))
            ):
                raise LexException.from_reader("invalid escape sequence \\" + c, self)
            escaping = False
            return 0

        return self.read_string_until(quote_closing, prefix, "f" in prefix.lower())

    ###
    # Special annotations
    ###

    @reader_for("'", ("quote",))
    @reader_for("`", ("quasiquote",))
    def tag_as(root):
        def _tag_as(self, _):
            nc = self.peekc()
            if (
                not nc
                or isnormalizedspace(nc)
                or self.reader_table.get(nc) == self.INVALID
            ):
                raise LexException.from_reader(
                    "Could not identify the next token.", self
                )
            model = self.parse_one_form()
            return mkexpr(root, model)

        return _tag_as

    @reader_for("~")
    def unquote(self, key):
        nc = self.peekc()
        if not nc or isnormalizedspace(nc) or self.reader_table.get(nc) == self.INVALID:
            return sym(key)
        return mkexpr(
            "unquote" + ("-splice" if self.peek_and_getc("@") else ""),
            self.parse_one_form(),
        )

    ###
    # Sequences
    ###

    @reader_for("(", (Expression, ")"))
    @reader_for("[", (List, "]"))
    @reader_for("{", (Dict, "}"))
    @reader_for("#{", (Set, "}"))
    @reader_for("#(", (Tuple, ")"))
    def sequence(seq_type, closer):
        return lambda self, _: seq_type(self.parse_forms_until(closer))

    ###
    # Reader tag-macros
    ###

    @reader_for("#")  # this is tag dispatch.
    def tag_dispatch(self, key):
        """General handler for reader macros (and tag macros).

        Reads a full identifier after the `#` and calls the corresponding handler
        (this allows, e.g., `#reads-multiple-forms foo bar baz`).

        Failing that, reads a single character after the `#` and immediately
        calls the corresponding handler (this allows, e.g., `#*args` to parse
        as `#*` followed by `args`).
        """

        if not self.peekc():  # another raise from another thing.
            raise PrematureEndOfInput.from_reader(
                "Premature end of input while attempting dispatch", self
            )

        if self.peek_and_getc("^"):
            typ = self.parse_one_form()
            target = self.parse_one_form()
            return mkexpr("annotate", target, typ)

        tag = None
        # try dispatching tagged ident
        ident = self.read_ident(just_peeking=True)
        if ident and mangle(key + ident) in self.reader_table:
            self.getn(len(ident))
            tag = mangle(key + ident)
        # failing that, dispatch tag + single character
        elif key + self.peekc() in self.reader_table:
            tag = key + self.getc()
        if tag:
            tree = self.dispatch(tag)
            return as_model(tree) if tree is not None else None

        raise LexException.from_reader(
            f"reader macro '{key + self.read_ident()}' is not defined", self
        )

    @reader_for("#_")
    def discard(self, _):
        """Discards the next parsed form."""
        self.parse_one_form()
        return None

    @reader_for("#*")
    def hash_star(self, _):
        """Unpacking forms `#*` and `#**`, corresponding to `*` and `**` in Python."""
        num_stars = 1
        while self.peek_and_getc("*"):
            num_stars += 1
        if num_stars > 2:
            raise LexException.from_reader("too many stars", self)
        return mkexpr(
            "unpack-" + ("iterable", "mapping")[num_stars - 1],
            self.parse_one_form(),
        )

    ###
    # Strings
    # (these are more complicated because f-strings
    #  form their own sublanguage)
    ###

    @reader_for("#[")
    def bracketed_string(self, _):
        """Bracketed strings. See the Hy docs for full details."""
        delim = []
        for c in self.chars():
            if c == "[":
                break
            elif c == "]":
                raise LexException.from_reader(
                    "Ran into a ']' where it wasn't expected.", self
                )
            delim.append(c)
        delim = "".join(delim)
        is_fstring = delim == "f" or delim.startswith("f-")

        # discard single initial newline, if any, accounting for all
        # three styles of newline
        self.peek_and_getc("\x0d")
        self.peek_and_getc("\x0a")

        index = -1

        def delim_closing(c):
            nonlocal index
            if c == "]":
                if index == len(delim):
                    # this is the second bracket at the end of the delim
                    return len(delim) + 2
                else:
                    # reset state, this may be the first bracket of closing delim
                    index = 0
            elif 0 <= index <= len(delim):
                # we're inside a possible closing delim
                if index < len(delim) and c == delim[index]:
                    index += 1
                else:
                    # failed delim, reset state
                    index = -1
            return 0

        return self.read_string_until(delim_closing, None, is_fstring, brackets=delim)

    def read_string_until(self, closing, prefix, is_fstring, **kwargs):
        if is_fstring:
            components = self.read_fcomponents_until(closing, prefix)
            return FString(components, **kwargs)
        s = self.read_chars_until(closing, prefix, is_fstring=False)
        return (Bytes if isinstance(s, bytes) else String)(s, **kwargs)

    def read_chars_until(self, closing, prefix, is_fstring):
        s = []
        for c in self.chars():
            s.append(c)
            # check if c is closing
            n_closing_chars = closing(c)
            if n_closing_chars:
                # string has ended
                s = s[:-n_closing_chars]
                break
            # check if c is start of component
            if is_fstring and c == "{":
                # check and handle "{{"
                if self.peek_and_getc("{"):
                    s.append("{")
                else:
                    # remove "{" from end of string component
                    s.pop()
                    break
        res = "".join(s).replace("\x0d\x0a", "\x0a").replace("\x0d", "\x0a")

        if prefix is not None:
            res = eval(f'{prefix}"""{res}"""')
        if is_fstring:
            return res, n_closing_chars
        return res

    def read_fcomponents_until(self, closing, prefix):
        components = []
        start = self.pos
        while True:
            s, closed = self.read_chars_until(closing, prefix, is_fstring=True)
            if s:
                components.append(self.fill_pos(String(s), start))
            if closed:
                break
            components.extend(self.read_fcomponent(prefix))
        return components

    def read_fcomponent(self, prefix):
        """May return one or two components, since the `=` debugging syntax
        will create a String component."""
        start = self.pos
        values = []
        conversion = None
        has_debug = False

        # read the expression, saving the text verbatim
        # in case we encounter debug `=`
        space_before = self.slurp_space()
        with self.saving_chars() as form_text:
            model = self.parse_one_form()
        space_between = self.slurp_space()

        # check for and handle debug syntax:
        # we emt the verbatim text before we emit the value
        if self.peek_and_getc("="):
            has_debug = True
            space_after = self.slurp_space()
            dbg_prefix = (
                space_before + "".join(form_text) + space_between + "=" + space_after
            )
            values.append(self.fill_pos(String(dbg_prefix), start))

        # handle conversion code
        if self.peek_and_getc("!"):
            conversion = self.getc()
        self.slurp_space()

        def component_closing(c):
            if c == "}":
                return 1
            return 0

        # handle formatting options
        format_components = []
        if self.peek_and_getc(":"):
            format_components = self.read_fcomponents_until(component_closing, prefix)
        else:
            if has_debug and conversion is None:
                conversion = "r"
            if not self.getc() == "}":
                raise LexException.from_reader("f-string: trailing junk in field", self)
        return values + [
            self.fill_pos(FComponent((model, *format_components), conversion), start)
        ]
