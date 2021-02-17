from django.apps import apps
from django.db import models

import pytest

from chemreg.substance.models import Substance


def test_substance_model():
    """Tests the validity of the Substance Model's attributes"""
    # Verify CharField attributes
    assert type(Substance.id.field) is models.CharField
    assert Substance.id.field.max_length == 50
    assert Substance.id.field.unique

    assert type(Substance.preferred_name.field) is models.CharField
    assert Substance.preferred_name.field.max_length == 255
    assert Substance.preferred_name.field.unique
    assert not Substance.preferred_name.field.blank

    assert type(Substance.display_name.field) is models.CharField
    assert Substance.display_name.field.max_length == 255
    assert Substance.display_name.field.unique
    assert not Substance.display_name.field.blank
    assert Substance.display_name.field.null

    assert type(Substance.description.field) is models.CharField
    assert Substance.description.field.max_length == 1024
    assert Substance.description.field.blank

    assert type(Substance.public_qc_note.field) is models.CharField
    assert Substance.public_qc_note.field.max_length == 1024
    assert Substance.public_qc_note.field.blank

    assert type(Substance.private_qc_note.field) is models.CharField
    assert Substance.private_qc_note.field.max_length == 1024
    assert Substance.private_qc_note.field.blank

    assert type(Substance.casrn.field) is models.CharField
    assert Substance.casrn.field.max_length == 50
    assert Substance.casrn.field.unique

    # Assert Foreign Key Attributes
    assert type(Substance.source.field) is models.ForeignKey
    assert Substance.source.field.related_model is apps.get_model("substance", "Source")

    assert type(Substance.substance_type.field) is models.ForeignKey
    assert Substance.substance_type.field.related_model is apps.get_model(
        "substance", "SubstanceType"
    )

    assert type(Substance.qc_level.field) is models.ForeignKey
    assert Substance.qc_level.field.related_model is apps.get_model(
        "substance", "QCLevelsType"
    )

    assert type(Substance.associated_compound.field) is models.OneToOneField
    assert Substance.associated_compound.field.related_model is apps.get_model(
        "compound", "BaseCompound"
    )

    assert Substance.relationships.field.model is apps.get_model(
        "substance", "SubstanceRelationship"
    )
    # Reverse lookup for relationships
    assert Substance.related_to.field.model is apps.get_model(
        "substance", "SubstanceRelationship"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "preferred_name,validity,code",
    [
        ("Valid String?", True, None),  # ? is a valid character
        ("Valid String'?", True, None),  # 277 ' is now a valid character
        ("Valid String*?", True, None),  # 289 * is now a valid character
        ("Valid String_?", True, None),  # 289 _ is now a valid character
        ("Valid String(?", True, None),  # 289 ( is now a valid character
        ("Valid String)?", True, None),  # 289 ) is now a valid character
        ("Valid String+?", True, None),  # 289 + is now a valid character
        ("Invalid String!", False, "invalid"),  # '!' is an invalid character
    ],
)
def test_validate_preferred_name(substance_factory, preferred_name, validity, code):
    substance = substance_factory.build(preferred_name=preferred_name)
    assert substance.is_valid() == validity
    if not validity:
        assert code == substance.errors["preferred_name"][0].code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "display_name,validity,code",
    [
        ("Valid String?", True, None),  # ? is a valid character
        ("Valid String'?", True, None),  # 277 ' is now a valid character
        ("Valid String*?", True, None),  # 289 * is now a valid character
        ("Valid String_?", True, None),  # 289 _ is now a valid character
        ("Valid String(?", True, None),  # 289 ( is now a valid character
        ("Valid String)?", True, None),  # 289 ) is now a valid character
        ("Valid String+?", True, None),  # 289 + is now a valid character
        ("Invalid String!", False, "invalid"),  # '!' is an invalid character
    ],
)
def test_validate_display_name(substance_factory, display_name, validity, code):
    substance = substance_factory.build(display_name=display_name)
    assert substance.is_valid() == validity
    if not validity:
        assert code == substance.errors["display_name"][0].code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "casrn,validity,code",
    [
        ("1234567-89-5", True, None),
        ("Non-CASRN String", False, "invalid"),  # invalid characters
        ("1-89-0", False, "invalid"),  # seg 1 too short
        ("12345678-89-0", False, "invalid"),  # seg 1 too long
        ("1234567-8-0", False, "invalid"),  # seg 2 too short
        ("12345678-890-0", False, "invalid"),  # seg2 too long
        ("1234567-89-", False, "invalid"),  # no checksum
        ("1234567-89-05", False, "invalid"),  # multiple checksums
        ("1234567-89-0", False, "checksum"),
    ],
)
def test_validate_casrn(substance_factory, casrn, validity, code):
    substance = substance_factory.build(casrn=casrn)
    assert substance.is_valid() == validity
    if substance.errors:
        assert substance.errors["casrn"][0].code == code


@pytest.mark.django_db
def test_substance_sid_unique_validation(substance_factory, defined_compound_factory):
    dc = defined_compound_factory().instance
    sub = substance_factory.build()
    sub.initial_data.update({"id": dc.pk})
    assert not sub.is_valid()
    assert sub.errors["id"][0].code == "invalid"
