from unittest.mock import patch

import pytest


@pytest.mark.django_db
def test_substance_save_signal(substance_factory):
    with patch("requests.post") as mocked_post:
        substance_factory()
        mocked_post.assert_called_once()


@pytest.mark.django_db
def test_substance_associate_compound(substance_factory, defined_compound_factory):
    # test to see this deletes the newly unorphaned compound
    substance = substance_factory.create(defined=True).instance
    with patch("requests.delete") as mocked_delete:
        substance.associated_compound = None
        substance.save()
        mocked_delete.assert_called_once()


@pytest.mark.django_db
def test_substance_disassociate_compound(substance_factory, defined_compound_factory):
    # test to see this adds an orphaned compound
    substance = substance_factory(defined=True).instance
    with patch("requests.post") as mocked_post:
        substance.associated_compound = None
        substance.save()
        mocked_post.assert_called_once()


@pytest.mark.django_db
def test_create_orphaned_compound(defined_compound_factory):
    # test to see orphaned compound adds a compound
    with patch("requests.post") as mocked_post:
        defined_compound_factory()
        mocked_post.assert_called_once()


@pytest.mark.django_db
def test_delete_orphaned_compound(defined_compound_factory):
    # test to see orphaned compound deletes compound (soft delete questions)
    compound = defined_compound_factory().instance
    with patch("requests.delete") as mocked_post:
        compound.delete()
        mocked_post.assert_called_once()


@pytest.mark.django_db
def test_synonym_save_signal(substance_factory, synonym_factory):
    with patch("requests.post") as mocked_post:
        # Create related resources
        substance = substance_factory().instance
        # Clear the mocks (related resources arent being tested
        mocked_post.reset_mock()

        synonym_factory(substance={"type": "substance", "id": substance.pk})
        # Assert synonym call was made
        mocked_post.assert_called_once()


@pytest.mark.django_db
def test_substance_delete_signal(substance_factory):
    with patch("requests.delete") as mocked_delete:
        sub = substance_factory().instance

        # Verify substance was never deleted
        mocked_delete.assert_not_called()

        sub.delete()

        # Verify substance was deleted
        mocked_delete.assert_called_once()


@pytest.mark.django_db
def test_synonym_delete_signal(substance_factory, synonym_factory):
    with patch("requests.post") as mocked_post, patch(
        "requests.delete"
    ) as mocked_delete:
        # Create related resources
        substance = substance_factory().instance
        syn = synonym_factory(
            substance={"type": "substance", "id": substance.pk}
        ).instance

        # Verify substance was never deleted & synonym sync mock is cleared
        mocked_delete.assert_not_called()
        mocked_post.reset_mock()

        syn.delete()

        # Assert substance is not deleted but is resynced
        mocked_delete.assert_not_called()
        mocked_post.assert_called_once()
