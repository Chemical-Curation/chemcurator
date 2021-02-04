import functools

from indigo import IndigoException


def catch_compound_calc_error(f):
    """
    A function wrapper for catching calculation errors.
    Primarially for catching 'indigo.IndigoException: element: bad valence...'
    errors and ensuring a 200 response.
    """

    @functools.wraps(f)
    def i(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IndigoException:
            pass

    return i
