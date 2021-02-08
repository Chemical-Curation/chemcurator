from pytest_factoryboy import register

from chemreg.compound.tests.factories import DefinedCompoundFactory
from chemreg.substance.tests.factories import (
    SubstanceFactory,
    SynonymFactory,
    SynonymQualityFactory,
    SynonymTypeFactory,
)

register(DefinedCompoundFactory)
register(SubstanceFactory)
register(SynonymFactory)
register(SynonymQualityFactory)
register(SynonymTypeFactory)
