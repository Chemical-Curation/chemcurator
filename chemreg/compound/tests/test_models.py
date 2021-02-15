from django.db import models

import pytest
from polymorphic.models import PolymorphicModel

from chemreg.compound.fields import StructureAliasField
from chemreg.compound.models import (
    BaseCompound,
    DefinedCompound,
    IllDefinedCompound,
    QueryStructureType,
    get_illdefined_qst,
)
from chemreg.compound.utils import build_cid
from chemreg.compound.validators import validate_inchikey_computable


def test_basecompound():
    assert issubclass(BaseCompound, PolymorphicModel)
    # cid
    id = BaseCompound._meta.get_field("id")
    assert isinstance(id, models.CharField)
    assert id.default == build_cid
    assert id.max_length == 50
    assert id.unique
    # structure
    structure = BaseCompound._meta.get_field("structure")
    assert isinstance(structure, models.TextField)


@pytest.mark.django_db
def test_definedcompound_validation(substance_factory, defined_compound_factory):
    sub = substance_factory().instance
    dc = defined_compound_factory.build()
    dc.initial_data.update({"id": sub.pk})
    assert not dc.is_valid()
    assert dc.errors["id"][0].code == "invalid"


def test_definedcompound():
    assert issubclass(DefinedCompound, BaseCompound)
    # molfile_v3000
    molfile_v3000 = DefinedCompound._meta.get_field("molfile_v3000")
    assert isinstance(molfile_v3000, StructureAliasField)
    assert validate_inchikey_computable in molfile_v3000.validators
    # inchikey
    inchikey = DefinedCompound._meta.get_field("inchikey")
    assert isinstance(inchikey, models.CharField)
    assert inchikey.max_length == 29


def test_illdefinedcompound():
    assert issubclass(IllDefinedCompound, BaseCompound)
    # mrvfile
    mrvfile = IllDefinedCompound._meta.get_field("mrvfile")
    assert isinstance(mrvfile, StructureAliasField)
    # query_structure_type
    query_structure_type = IllDefinedCompound._meta.get_field("query_structure_type")
    assert isinstance(query_structure_type, models.ForeignKey)
    assert query_structure_type.default == get_illdefined_qst


@pytest.mark.django_db
def test_illdefinedcompound_validation(substance_factory, ill_defined_compound_factory):
    sub = substance_factory().instance
    idc = ill_defined_compound_factory.build()
    idc.initial_data.update({"id": sub.pk})
    assert not idc.is_valid()
    assert idc.errors["id"][0].code == "invalid"


def test_querystructuretype():
    # name
    name = QueryStructureType._meta.get_field("name")
    assert isinstance(name, models.SlugField)
    assert name.max_length == 49
    assert name.unique
    # label
    label = QueryStructureType._meta.get_field("label")
    assert isinstance(label, models.CharField)
    assert label.max_length == 99
    assert label.unique
    # short_description
    short_description = QueryStructureType._meta.get_field("short_description")
    assert isinstance(short_description, models.CharField)
    assert short_description.max_length == 499
    # long_description
    long_description = QueryStructureType._meta.get_field("long_description")
    assert isinstance(long_description, models.TextField)
