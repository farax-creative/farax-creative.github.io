# Shared helpers for the per-product manual builders.
#
# Those builders work by taking the Zap Doctor manual as a shell and rewriting the parts
# that name the product. Every one of those rewrites is a str.replace or re.sub, and both
# fail the same way: if the text they look for is not there, they return the input
# unchanged and raise nothing. The output is then a complete, valid, well-formed manual
# that still says "Zap Doctor" somewhere -- exactly the kind of failure this site has
# shipped before (report/index.html went live with __FORM_URL__ in it for four days).
#
# build_zap_viewer_manual.py already carries a comment admitting one of these: the bug
# report link's ?product= parameter "arrives wrong and nothing complains -- a mismatched
# product lands in the form as a blank field, not an error."
#
# So: every rewrite goes through one of these two functions, and a rewrite that matches
# nothing is a build failure, not a silent pass.
import re


class ManualBuildError(AssertionError):
    """A rewrite the manual build depends on did not match anything."""


def must_replace(text, old, new, what, count=None):
    """str.replace, but the substring has to actually be there.

    `count` pins how many occurrences are expected when that number is part of the
    contract (the language switcher's per-language links, say). Left None, any number
    above zero passes.
    """
    found = text.count(old)
    if found == 0:
        raise ManualBuildError(
            "%s: nothing to replace -- the template no longer contains %r" % (what, old))
    if count is not None and found != count:
        raise ManualBuildError(
            "%s: expected %d occurrence(s) of %r, found %d" % (what, count, old, found))
    return text.replace(old, new)


def must_sub(pattern, repl, text, what, flags=0, count=None):
    """re.sub, but the pattern has to actually match."""
    out, n = re.subn(pattern, repl, text, flags=flags)
    if n == 0:
        raise ManualBuildError(
            "%s: pattern matched nothing -- %s" % (what, pattern))
    if count is not None and n != count:
        raise ManualBuildError(
            "%s: expected %d match(es), got %d -- %s" % (what, count, n, pattern))
    return out


def may_sub(pattern, repl, text, flags=0):
    """re.sub for a rewrite that is genuinely optional.

    Use this only where matching nothing is a real, expected state -- not as an escape
    hatch when must_sub is inconvenient. Every call should say in a comment why zero
    matches is fine.
    """
    return re.sub(pattern, repl, text, flags=flags)
