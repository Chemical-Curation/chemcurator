from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from chemreg.resolution.indices import CompoundIndex, SubstanceIndex

# Todo: Syncs on:
#   - Substance Associate  compound needs to be dis
#   - Substance Disassociate
#   - Orphan Compound Save
#   - Orphan Compound Delete


@receiver(post_save, sender=apps.get_model("substance.Substance"))
@receiver(post_delete, sender=apps.get_model("substance.Substance"))
def substance_index_substance_sync(instance, **kwargs):
    """Post save signal to sync resolver app with chemreg's substance

    Args:
        instance (:obj:`Substance`): Substance being updated.
    """

    # This is incomplete.  This is where i'm planning on handing delete and save requests on orphan compounds
    if instance.original_compound and not instance.associated_compound:
        CompoundIndex().delete(instance.original_compound.pk)

    # bool determining if this is coming from post_save or post_delete
    delete = kwargs.get("created") is None
    if instance:
        SubstanceIndex().sync_instances(instance, delete)


@receiver(post_save, sender=apps.get_model("substance.Synonym"))
@receiver(post_delete, sender=apps.get_model("substance.Synonym"))
def substance_index_synonym_sync(instance, **kwargs):
    """Post save signal to sync resolver app with chemreg's synonyms

    Args:
        instance (:obj:`Synonym`): Synonym being updated.
    """
    if instance:
        SubstanceIndex().sync_instances(instance.substance)
