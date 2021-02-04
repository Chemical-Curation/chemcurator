import functools
from typing import Any

from indigo import IndigoException


def catch_compound_calc_error(f: Any) -> Any:
    """
    A function wrapper for catching calculation errors.
    Primarially for catching 'indigo.IndigoException: element: bad valence...'
    errors and ensuring a 200 response.

    Args:
        f: a function to be wrapped.

    Returns:
        Either a calculated value (MW, MF, SMILES, Inchikey) or `null`

    """

    @functools.wraps(f)
    def i(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IndigoException:
            pass

    return i
