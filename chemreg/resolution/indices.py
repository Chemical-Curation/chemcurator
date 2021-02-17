import json

from django.apps import apps

from rest_framework.exceptions import APIException

import requests
from config.settings import RESOLUTION_URL


class Index:
    """ChemCurator to interface with the resolver app."""

    HEADERS = {"Content-Type": "application/vnd.api+json"}

    def __init__(self, fail_silently=True):
        self.fail_silently = fail_silently

        for attr in ["index_url", "search_url", "delete_url", "delete_pk"]:
            assert getattr(
                self, attr
            ), "Class {index_class} missing {attr} attribute".format(
                index_class=self.__class__.__name__, attr=attr
            )

    def sync_instances(self, instances, delete=False):
        """Posts instance(s) to resolver.

        Args:
            instances (`list` of `:obj:` or :obj:): model instances to be saved in resolver
            delete (bool): Whether this will add or remove the instance
        """
        try:  # Attempt to iterate instances
            for instance in instances:
                self._sync_instance(instance, delete)
        except TypeError:  # Assume solo instance
            self._sync_instance(instances, delete)

    def _sync_instance(self, instance, delete):
        """Handles the posting of an instance to resolver.

        Args:
            instance (:obj:Substance): Substances to be saved in resolver
        """
        #  add the instance
        if not delete:
            model_document = self.get_model_document(instance)
            data = json.dumps(model_document)
            try:
                requests.post(self.index_url, data, headers=self.HEADERS)
            except requests.exceptions.ConnectionError as conn_err:
                if not self.fail_silently:
                    raise conn_err
        # remove the instance
        else:
            try:
                requests.delete(
                    self.delete_url + getattr(instance, self.delete_pk),
                    headers=self.HEADERS,
                )
            except requests.exceptions.ConnectionError as conn_err:
                if not self.fail_silently:
                    raise conn_err

    def delete_all_instances(self):
        try:
            requests.delete(self.index_url, headers=self.HEADERS)
        except requests.exceptions.ConnectionError as conn_err:
            if not self.fail_silently:
                raise conn_err

    def search(self, term):
        try:
            resp = requests.get(
                self.search_url, params={"identifier": term}, headers=self.HEADERS
            )
            return resp.json()
        except requests.exceptions.ConnectionError:
            raise APIException("The Resolver service is not available right now")
        except Exception as e:
            raise APIException(detail=str(e))

    def get_model_document(self, instance):
        raise NotImplementedError("`get_model_document()` must be implemented.")

    def delete(self, pk):
        # delete a single row
        try:
            resp = requests.delete(self.delete_url + pk, headers=self.HEADERS)
            return resp.json()
        except requests.exceptions.ConnectionError:
            raise APIException("The Resolver service is not available right now")
        except Exception as e:
            raise APIException(detail=str(e))


class SubstanceIndex(Index):
    search_url = f"{RESOLUTION_URL}/api/v1/resolver"
    index_url = f"{RESOLUTION_URL}/api/v1/substances/_index"
    delete_url = f"{RESOLUTION_URL}/api/v1/substances/"
    delete_pk = "pk"

    def get_model_document(self, instance):
        SYNONYM_DEFAULT_WEIGHT = 1
        SYNONYM_DEFAULT_SCORE_MODIFIER = 0
        return {
            "data": {
                "id": instance.pk,
                "type": "substance",
                "attributes": {
                    "identifiers": {
                        "compound_id": instance.associated_compound_id,
                        "inchikey": instance.associated_compound.inchikey
                        if isinstance(
                            instance.associated_compound,
                            apps.get_model("compound.DefinedCompound"),
                        )
                        else None,
                        "preferred_name": instance.preferred_name,
                        "display_name": instance.display_name,
                        "casrn": instance.casrn,
                        "synonyms": [
                            {
                                "identifier": synonym.identifier,
                                "weight": (
                                    synonym.synonym_quality.score_weight
                                    if synonym.synonym_quality
                                    else SYNONYM_DEFAULT_WEIGHT
                                )
                                + (
                                    synonym.synonym_type.score_modifier
                                    if synonym.synonym_type
                                    else SYNONYM_DEFAULT_SCORE_MODIFIER
                                ),
                                "synonymtype": synonym.synonym_type.label,
                            }
                            for synonym in instance.synonym_set.all()
                        ],
                    },
                },
            }
        }


class CompoundIndex(Index):
    search_url = f"{RESOLUTION_URL}/api/v1/resolver"
    index_url = f"{RESOLUTION_URL}/api/v1/substances/_index"
    delete_url = f"{RESOLUTION_URL}/api/v1/substances/"
    delete_pk = "pk"

    def get_model_document(self, instance):
        return {
            "data": {
                "id": instance.pk,
                "type": "substance",  # todo: index name
                "attributes": {
                    "identifiers": {
                        "compound_id": instance.pk,
                        "inchikey": instance.inchikey
                        if isinstance(
                            instance, apps.get_model("compound.DefinedCompound"),
                        )
                        else None,
                        "preferred_name": None,
                        "display_name": None,
                        "casrn": None,
                        "synonyms": [],
                    },
                },
            }
        }
