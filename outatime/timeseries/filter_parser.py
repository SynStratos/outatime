import lark
from lark import v_args

grammar = """
    ?start: expression

    ?expression: "(" expression ")"
        | NOT_OP expression -> negate_expr
        | expression BIN_OP expression -> make_expr
        | filter

    NOT_OP: "~"
        | "not"

    BIN_OP: "&"
        | "|"
        | "^"
        | "and"
        | "or"
        | "xor"

    ?filter: period OPERATOR sum -> make_filter
        | sum OPERATOR period -> make_rev_filter
        | filter OPERATOR sum -> combine_filters

    OPERATOR: "=="
        | "!="
        | ">"
        | ">="
        | "<"
        | "<="

    !period: "day" -> period_name
        | "month" -> period_name
        | "year" -> period_name
    
    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div
        | product "//" atom -> floordiv
        | product "%" atom -> mod
        | product "**" atom -> pow

    ?atom: NUMBER -> number
         | "-" atom -> neg
         | "(" sum ")"
         | "|" sum "|" -> abs
         | "|" atom "|" -> abs

    %import common.CNAME -> NAME
    %import common.WORD -> WORD
    %import common.NUMBER -> NUMBER
    %import common.WS_INLINE
    %import common.STRING -> STRING

    %ignore WS_INLINE
"""


@v_args(inline=True)
class FilterParser(lark.Transformer):
    import operator
    from operator import add, truediv as div, mul, sub, neg, mod, floordiv, pow, abs
    number = float
    period_name = str

    operators = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
    }

    bin_operators = {
        "&": operator.and_,
        "|": operator.or_,
        "^": operator.xor,
        "and": operator.and_,
        "or": operator.or_,
        "xor": operator.xor
    }

    def make_expr(self, expr_a, bin_op, expr_b):
        """Parse a binary expression."""
        expr_a, _ = expr_a
        expr_b, _ = expr_b

        def _f(x):
            return self.bin_operators[bin_op](expr_a(x), expr_b(x))

        return _f, None

    @staticmethod
    def negate_expr(_, expr):
        """Parse a negated expression."""
        expr, _ = expr

        def _f(x):
            return not expr(x)

        return _f, None

    def make_filter(self, period, op, value):
        """Parse a filter in the order KEY - OPERATOR - VALUE."""

        def _f(x):
            return self.operators[op](getattr(x.day, period), int(value))

        return _f, period

    def make_rev_filter(self, value, op, period):
        """Parse a filter in the order VALUE - OPERATOR - KEY."""

        def _f(x):
            return self.operators[op](int(value), getattr(x.day, period))

        return _f, period

    def combine_filters(self, filter_res, op, value):
        """Parse a combination of filters."""
        _filter, period = filter_res

        def _f(x):
            return _filter(x) and self.operators[op](getattr(x.day, period), int(value))

        return _f, period

    def get_parser(self):
        """Generate a parser method to use with the given grammar."""
        lark_parser = lark.Lark(grammar, parser='lalr', transformer=self.__class__())

        @staticmethod
        def _parse(query):
            try:
                return lark_parser.parse(query)
            except:
                raise FilterParserError("Bad query string.")

        return _parse


class FilterParserError(Exception):
    msg = "Bad query string."

    def __init__(self, msg=msg, *args):
        super().__init__(msg, *args)
