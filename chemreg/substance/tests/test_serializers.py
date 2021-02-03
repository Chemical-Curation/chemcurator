import pytest
from rest_framework_json_api.utils import get_included_serializers

from chemreg.common.serializers import CommonInfoSerializer
from chemreg.compound.serializers import CompoundSerializer
from chemreg.substance.serializers import (
    QCLevelsTypeSerializer,
    RelationshipTypeSerializer,
    SourceSerializer,
    SubstanceRelationshipSerializer,
    SubstanceSerializer,
    SubstanceTypeSerializer,
    SynonymQualitySerializer,
    SynonymSerializer,
    SynonymTypeSerializer,
)


@pytest.mark.django_db
def test_qc_levels_type_serializer():
    assert issubclass(QCLevelsTypeSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_qc_levels_type(qc_levels_type_factory):
    serializer = qc_levels_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_synonym_type_serializer():
    assert issubclass(SynonymTypeSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_synonym_type(synonym_type_factory):
    serializer = synonym_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_source_serializer():
    assert issubclass(SourceSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_source(source_factory):
    serializer = source_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_serializer():
    assert issubclass(SubstanceSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_substance_blankable_fields(substance_factory):
    substance = substance_factory.build(
        description="", public_qc_note="", private_qc_note=""
    )
    assert substance.is_valid()


@pytest.mark.django_db
def test_substance_serializer_includes():
    serializer = get_included_serializers(SubstanceSerializer)
    assert serializer["source"] is SourceSerializer
    assert serializer["substance_type"] is SubstanceTypeSerializer
    assert serializer["qc_level"] is QCLevelsTypeSerializer
    assert serializer["associated_compound"] is CompoundSerializer


@pytest.mark.django_db
def test_unique_name_field_on_substance(
    substance_factory, synonym_factory, synonym_quality_factory
):
    """ This test verifies that a substance will have a unique name across the
    "preferred_name", "display_name", "casrn", and "synonym.identifier" fields
    upon creation or update amongst all existing in the db.
    """
    synonym_quality = synonym_quality_factory.create(is_restrictive=True).instance
    synonym = synonym_factory.create(
        identifier="47474-74-8",  # has to be valid for CASRN, see below
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    ).instance
    sub1 = substance_factory.create(
        # these fields need to pass casrn validation when passed to that attr
        preferred_name="4747-47-1",
        display_name="47-47-2",
    ).instance

    err_msg = "The identifier/s ['{}'] is not unique in restrictive name fields."

    sub2 = substance_factory.build(display_name=sub1.preferred_name)
    assert not sub2.is_valid()
    assert (
        err_msg.format(sub1.preferred_name)[:47] in sub2.errors["non_field_errors"][0]
    )
    sub2 = substance_factory.build(display_name=sub1.casrn)
    assert not sub2.is_valid()
    assert err_msg.format(sub1.casrn)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(display_name=synonym.identifier)
    assert not sub2.is_valid()
    assert err_msg.format(synonym.identifier)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(casrn=sub1.preferred_name)
    assert not sub2.is_valid()
    assert (
        err_msg.format(sub1.preferred_name)[:47] in sub2.errors["non_field_errors"][0]
    )
    sub2 = substance_factory.build(casrn=sub1.display_name)
    assert not sub2.is_valid()
    assert err_msg.format(sub1.display_name)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(casrn=synonym.identifier)
    assert not sub2.is_valid()
    assert err_msg.format(synonym.identifier)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(preferred_name=sub1.display_name)
    assert not sub2.is_valid()
    assert err_msg.format(sub1.display_name)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(preferred_name=sub1.casrn)
    assert not sub2.is_valid()
    assert err_msg.format(sub1.casrn)[:47] in sub2.errors["non_field_errors"][0]
    sub2 = substance_factory.build(preferred_name=synonym.identifier)
    assert not sub2.is_valid()
    assert err_msg.format(synonym.identifier)[:47] in sub2.errors["non_field_errors"][0]


@pytest.mark.django_db
def test_substance_no_associated_compound(substance_factory):
    serializer = substance_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_defined_compound(substance_factory):
    serializer = substance_factory.build(defined=True)
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_ill_defined_compound(substance_factory):
    serializer = substance_factory.build(illdefined=True)
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_unique_compound(substance_factory):
    substance = substance_factory.create(defined=True).instance
    compound = substance.associated_compound
    obj = {"id": compound.id, "type": "definedCompound"}
    serializer = substance_factory.build(associated_compound=obj)
    assert not serializer.is_valid()
    assert (
        str(serializer.errors["associated_compound"][0])
        == "Compound ID value violates unique constraint"
    )


@pytest.mark.django_db
def test_substance_type_serializer():
    assert issubclass(SubstanceTypeSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_substance_type(substance_type_factory):
    serializer = substance_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_relationship_type_serializer():
    assert issubclass(RelationshipTypeSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_relationship_type(relationship_type_factory):
    serializer = relationship_type_factory.build()
    assert serializer.is_valid()
    serializer.save()


def test_synonym_quality_serializer():
    assert issubclass(SynonymQualitySerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_synonym_quality(synonym_quality_factory):
    serializer = synonym_quality_factory.build()
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_synonym_quality_score_weight_validation(synonym_quality_factory):
    model_dict = synonym_quality_factory.build().initial_data
    # Negative score_weights are forbidden
    model_dict.update(score_weight=-1.0)
    assert not SynonymQualitySerializer(data=model_dict).is_valid()


@pytest.mark.django_db
def test_synonym_serializer():
    assert issubclass(SynonymSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_synonym_serializer_includes():
    serializer = get_included_serializers(SynonymSerializer)
    assert serializer["source"] is SourceSerializer
    assert serializer["substance"] is SubstanceSerializer
    assert serializer["synonym_quality"] is SynonymQualitySerializer
    assert serializer["synonym_type"] is SynonymTypeSerializer


@pytest.mark.django_db
def test_synonym_validation_regular_expression(synonym_factory, synonym_type_factory):
    synonym_type = synonym_type_factory(
        validation_regular_expression="^[0-9]{2,7}-[0-9]{2,7}-[0-9]$"
    ).instance

    synonym_correct = synonym_factory.build(
        identifier="1234567-89-5",
        synonym_type={"type": "synonymType", "id": synonym_type.pk},
    )

    synonym_invalid_format = synonym_factory.build(
        identifier="12345678-89-5",
        synonym_type={"type": "synonymType", "id": synonym_type.pk},
    )

    assert synonym_correct.is_valid()
    assert not synonym_correct.errors
    synonym_correct.save()

    # Test that updates are retested for invalidity
    synonym_invalid_update = SynonymSerializer(
        synonym_correct.instance, {"identifier": "12345678-89-5"}, partial=True
    )
    assert not synonym_invalid_update.is_valid()
    assert synonym_invalid_update.errors

    assert not synonym_invalid_format.is_valid()
    assert synonym_invalid_format.errors


@pytest.mark.django_db
def test_synonym_identifier_unique(
    substance_factory, synonym_factory, synonym_quality_factory
):
    """ This test verifies that a synonym.identifier will have a unique name across the
    "preferred_name", "display_name", "casrn", and "synonym.identifier" fields
    upon creation or update amongst all existing in the db.
    """
    substance = substance_factory.create().instance
    synonym_quality = synonym_quality_factory.create(is_restrictive=True).instance
    quality_data = {"type": "synonymQuality", "id": synonym_quality.pk}
    syn1 = synonym_factory.create(
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    ).instance

    err_msg = "The identifier '{}' is not unique in restrictive name fields."

    syn2 = synonym_factory.build(
        identifier=substance.preferred_name, synonym_quality=quality_data,
    )
    assert not syn2.is_valid()
    assert (
        err_msg.format(substance.preferred_name)[:47]
        in syn2.errors["non_field_errors"][0]
    )
    syn2 = synonym_factory.build(
        identifier=substance.display_name, synonym_quality=quality_data,
    )
    assert not syn2.is_valid()
    assert (
        err_msg.format(substance.display_name)[:47]
        in syn2.errors["non_field_errors"][0]
    )
    syn2 = synonym_factory.build(
        identifier=substance.casrn, synonym_quality=quality_data,
    )
    assert not syn2.is_valid()
    assert err_msg.format(substance.casrn)[:47] in syn2.errors["non_field_errors"][0]
    syn2 = synonym_factory.build(identifier=syn1.identifier)
    syn2 = synonym_factory.build(
        identifier=syn1.identifier, synonym_quality=quality_data,
    )
    assert not syn2.is_valid()
    assert err_msg.format(syn1.identifier)[:47] in syn2.errors["non_field_errors"][0]


@pytest.mark.django_db
def test_synonym_type_validation_regular_expression(
    synonym_factory, synonym_type_factory,
):
    """ This test verifies that if a synonym type has its
    validation_regular_expression updated.  All synonyms attached must pass validation.
    """

    # Create 2 synonym types with no validation constraint
    synonym_type_valid = synonym_type_factory(
        validation_regular_expression=".*"
    ).instance
    synonym_type_invalid = synonym_type_factory(
        validation_regular_expression=".*"
    ).instance

    # Attach a synonym to the synonym type created above.  The identifier
    #   will decide whether validation_regular_expression can be changed without error.
    synonym_factory(
        identifier="1234567-89-0",
        synonym_type={"type": "synonymType", "id": synonym_type_invalid.pk},
    )  # valid
    synonym_factory(
        identifier="12345678-89-0",
        synonym_type={"type": "synonymType", "id": synonym_type_invalid.pk},
    )  # invalid

    # Test Valid
    # Partial update validation_regular_expression and validate
    synonym_type_valid_serializer = SynonymTypeSerializer(
        synonym_type_valid,
        data={"validation_regular_expression": "^[0-9]{2,7}-[0-9]{2,7}-[0-9]$"},
        partial=True,
    )
    assert synonym_type_valid_serializer.is_valid()
    assert not synonym_type_valid_serializer.errors
    synonym_type_valid_serializer.save()

    # Revert back to false.
    synonym_type_valid_revert_to_false = SynonymTypeSerializer(
        synonym_type_valid_serializer.instance,
        data={"validation_regular_expression": ".*"},
        partial=True,
    )
    assert synonym_type_valid_revert_to_false.is_valid()
    assert not synonym_type_valid_revert_to_false.errors
    synonym_type_valid_revert_to_false.save()

    # Test Invalid
    synonym_type_invalid_serializer = SynonymTypeSerializer(
        synonym_type_invalid,
        data={"validation_regular_expression": "^[0-9]{2,7}-[0-9]{2,7}-[0-9]$"},
        partial=True,
    )
    assert not synonym_type_invalid_serializer.is_valid()
    assert synonym_type_invalid_serializer.errors
    assert (
        "invalid_data"
        == synonym_type_invalid_serializer.errors["non_field_errors"][0].code
    )


@pytest.mark.django_db
def test_synonym_validates_synonym_type_is_casrn(synonym_factory, synonym_type_factory):
    """ This test verifies that if a synonym type has is_casrn set to True,
    synonyms that are added are only permitted if they meet valid CAS-RN checksum.
    """
    synonym_type = synonym_type_factory(
        is_casrn=True, validation_regular_expression=".*"
    ).instance

    synonym_correct = synonym_factory.build(
        identifier="1234567-89-5",
        synonym_type={"type": "synonymType", "id": synonym_type.pk},
    )

    synonym_invalid_checksum = synonym_factory.build(
        identifier="1234567-89-0",
        synonym_type={"type": "synonymType", "id": synonym_type.pk},
    )

    assert synonym_correct.is_valid()
    assert not synonym_correct.errors
    synonym_correct.save()

    # Test that updates are retested for invalidity
    synonym_invalid_update = SynonymSerializer(
        synonym_correct.instance, {"identifier": "1234567-89-0"}, partial=True
    )
    assert not synonym_invalid_update.is_valid()
    assert synonym_invalid_update.errors

    assert not synonym_invalid_checksum.is_valid()
    assert synonym_invalid_checksum.errors


@pytest.mark.django_db
def test_synonym_type_validates_is_casrn(synonym_factory, synonym_type_factory):
    """ This test verifies that if a synonym type is set where `is_casrn = False`,
    and a user requests the `is_casrn = True`, the change will only happen if all
    child synonym identifiers are valid.
    """

    # Create 2 synonym types, both with CAS-RN false
    synonym_type_valid = synonym_type_factory(
        is_casrn=False, validation_regular_expression="^[0-9]{2,7}-[0-9]{2,7}-[0-9]$"
    ).instance
    synonym_type_invalid = synonym_type_factory(
        is_casrn=False, validation_regular_expression="^[0-9]{2,7}-[0-9]{2,7}-[0-9]$"
    ).instance

    # Attach a valid casrn to one and an invalid casrn to the other.
    synonym_factory(
        identifier="1234567-89-5",
        synonym_type={"type": "synonymType", "id": synonym_type_valid.pk},
    )  # valid
    synonym_factory(
        identifier="1234567-89-0",
        synonym_type={"type": "synonymType", "id": synonym_type_invalid.pk},
    )  # invalid

    # Partial update, Validate, and Save
    synonym_type_valid_serializer = SynonymTypeSerializer(
        synonym_type_valid, data={"is_casrn": True}, partial=True
    )
    assert synonym_type_valid_serializer.is_valid()
    assert not synonym_type_valid_serializer.errors
    synonym_type_valid_serializer.save()

    synonym_type_valid_revert_to_false = SynonymTypeSerializer(
        synonym_type_valid_serializer.instance, data={"is_casrn": True}, partial=True
    )
    assert synonym_type_valid_revert_to_false.is_valid()
    assert not synonym_type_valid_revert_to_false.errors
    synonym_type_valid_revert_to_false.save()

    synonym_type_invalid_serializer = SynonymTypeSerializer(
        synonym_type_invalid, data={"is_casrn": True}, partial=True
    )
    assert not synonym_type_invalid_serializer.is_valid()
    assert synonym_type_invalid_serializer.errors
    assert (
        "invalid_data"
        == synonym_type_invalid_serializer.errors["non_field_errors"][0].code
    )


@pytest.mark.django_db
def test_substance_relationship_serializer():
    assert issubclass(SubstanceRelationshipSerializer, CommonInfoSerializer)


@pytest.mark.django_db
def test_substance_relationship_serializer_includes():
    serializer = get_included_serializers(SubstanceRelationshipSerializer)
    assert serializer["from_substance"] is SubstanceSerializer
    assert serializer["to_substance"] is SubstanceSerializer
    assert serializer["source"] is SourceSerializer
    assert serializer["relationship_type"] is RelationshipTypeSerializer


@pytest.mark.django_db
def test_is_restrictive_on_synonyms(synonym_factory, synonym_quality_factory):
    """ This test verifies that if a synonym quality has the is_restrictive field
    set to True, associated synonym.identifier fields will be validated to be unique.
    """
    synonym_quality = synonym_quality_factory.create(is_restrictive=False).instance

    synonym_factory.create(
        identifier="1234567-89-5",
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    )
    syn2 = synonym_factory.build(
        identifier="1234567-89-5",
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    )
    assert syn2.is_valid()  # if False, they can have the same names

    synonym_quality = synonym_quality_factory.create(is_restrictive=True).instance

    synonym_factory.create(
        identifier="1234567-89-5",
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    )
    syn2 = synonym_factory.build(
        identifier="1234567-89-5",
        synonym_quality={"type": "synonymQuality", "id": synonym_quality.pk},
    )
    assert not syn2.is_valid()  # if True, same name is restricted
    assert (
        syn2.errors["non_field_errors"][0]
        == "The identifier '1234567-89-5' is not unique in restrictive name fields."
    )


@pytest.mark.django_db
def test_substance_display_name_null(substance_factory):
    serializer = substance_factory.build(display_name=None)
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_substance_casrn_null(substance_factory):
    serializer = substance_factory.build(casrn=None)
    assert serializer.is_valid()
    serializer.save()


@pytest.mark.django_db
def test_bug_263(substance_factory, synonym_factory, synonym_quality_factory):
    """ If I create the synonym "water" and associated it with a restrictive
    synonym quality, I should still be able to create the synonym "water" as a
    synonym associated with a non-restrictive synonym.
    """
    restricted_quality = synonym_quality_factory.create(is_restrictive=True).instance
    unrestricted_quality = synonym_quality_factory.create(is_restrictive=False).instance
    synonym = synonym_factory.create(
        identifier="water",  # has to be valid for CASRN
        synonym_quality={"type": "synonymQuality", "id": restricted_quality.pk},
    ).instance
    synonym2 = synonym_factory.create(
        identifier="water",  # same identifier, but unrestricted
        synonym_quality={"type": "synonymQuality", "id": unrestricted_quality.pk},
    ).instance
    assert synonym.identifier == synonym2.identifier
