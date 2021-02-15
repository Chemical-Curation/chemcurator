from pytest_factoryboy import register

from chemreg.compound.tests.factories import (
    DefinedCompoundFactory,
    IllDefinedCompoundFactory,
)
from chemreg.substance.tests.factories import (
    SubstanceFactory,
    SynonymFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(DefinedCompoundFactory)
register(IllDefinedCompoundFactory)
register(SubstanceFactory)
register(SynonymFactory)
register(SynonymQualityFactory)
register(SynonymTypeFactory)
