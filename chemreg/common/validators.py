import re

from django.apps import apps
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import UniqueTogetherValidator
from rest_framework.validators import qs_exists

from chemreg.common.utils import casrn_checksum


def validate_deprecated(vocab):
    """Validates that the ControlledVocabulary is not deprecated.

    Args:
        vocab: the ControlledVocabulary object ("QueryStructureType", "SubstanceType")

    Raises:
        ValidationError: If the vocab is deprecated.
    """
    if vocab.deprecated:
        raise ValidationError(
            f"The {vocab._meta.object_name} submitted is no longer supported."
        )
    return vocab


def validate_casrn_checksum(value):
    """ Validates a CAS-RN's checksum value

    https://en.wikipedia.org/wiki/CAS_Registry_Number#Format

    Args:
        value (str): A formatted CAS-RN string.
            Format should be 2-7 digits hyphen 2 digits hyphen 1 digit.
            The last digit is a checksum of the previous digits.
            For example water is 7732-18-5.
            (8×1 + 1×2 + 2×3 + 3×4 + 7×5 + 7×6) = 105
            105 % 10 = 5

    Raises:
        ValidationError: The provided checksum is invalid

    """
    value_stripped = re.sub("[^0-9]", "", value)  # Strip all non-digits
    if len(value_stripped) < 5:
        return  # the value will not pass formatting validation
    if value_stripped and int(value_stripped[-1]) != casrn_checksum(
        int(value_stripped[:-1])
    ):
        raise ValidationError(
            "Provided CAS-RN does not meet checksum requirements.", "checksum"
        )


def validate_is_regex(value):
    """ Validates a string is valid re regex

    https://docs.python.org/3/library/re.html#regular-expression-syntax

    Args:
        value (str): A valid regex string

    Raises:
        ValidationError: The provided RegExp is invalid
    """
    try:
        re.compile(value)
    except re.error:
        raise ValidationError("The provided RegExp is invalid")


@deconstructible
class UniqueAcrossModelsValidator:
    model_list = []
    message = _("Value is not unique.")
    code = "invalid"

    def __init__(self, model_list=None, message=None, code=None):
        if model_list is not None:
            self.model_list = model_list
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Validate that the input is not contained within any other model/key pair
        """
        for model in self.model_list:
            if apps.get_model(model).objects.filter(pk=value).exists():
                raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, UniqueAcrossModelsValidator)
            and self.model_list == other.model_list
            and (self.message == other.message)
            and (self.code == other.code)
        )


class ExternalIdUniqueTogetherValidator(UniqueTogetherValidator):
    """
        A validator that will allow for a custom error message.
    """

    def __init__(self, queryset, fields, message=None, duplicate_field=None):
        self.queryset = queryset
        self.fields = fields
        self.message = message or self.message
        self.duplicate_field = duplicate_field

    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset, serializer)
        queryset = self.exclude_current_instance(attrs, queryset, serializer.instance)

        # Ignore validation if any field is None
        checked_values = [
            value for field, value in attrs.items() if field in self.fields
        ]
        if None not in checked_values and qs_exists(queryset):
            duplicated_record = queryset.values_list(
                self.duplicate_field, flat=True
            ).first()
            message = self.message.format(duplicate_field=duplicated_record)
            raise ValidationError(message, code="unique")
