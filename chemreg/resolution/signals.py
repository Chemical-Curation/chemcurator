from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from chemreg.resolution.indices import CompoundIndex, SubstanceIndex

# Todo: Syncs:
#   Cases:
#   - Compound saved compound needs to be sent to resolver
#   - Compound deleted compound needs to be removed from resolver
#   - Substance saved w/ associated_compound  compound needs to be removed from resolver
#   - Substance saved w/o associated_compound  if compound existed, compound needs to be sent to resolver


@receiver(post_save, sender=apps.get_model("substance.Substance"))
@receiver(post_delete, sender=apps.get_model("substance.Substance"))
def substance_index_substance_sync(instance, **kwargs):
    """Post save signal to sync resolver app with chemreg's substance

    Args:
        instance (:obj:`Substance`): Substance being updated.
    """

    # This is incomplete.  This is where i'm planning on handing delete and save requests on orphan compounds
    if instance.associated_compound:
        CompoundIndex().delete(instance.associated_compound.pk)
    if instance.original_compound and not instance.associated_compound:
        CompoundIndex().sync_instances(instance.original_compound)

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


@receiver(post_save, sender=apps.get_model("compound.DefinedCompound"))
@receiver(post_delete, sender=apps.get_model("compound.DefinedCompound"))
@receiver(post_save, sender=apps.get_model("compound.illDefinedCompound"))
@receiver(post_delete, sender=apps.get_model("compound.illDefinedCompound"))
def substance_index_compound_sync(instance, **kwargs):
    """Post save signal to sync resolver app with chemreg's compound

    Args:
        instance (:obj:`Compound`): Compound being updated, either Defined or IllDefined.
    """

    # bool determining if this is coming from post_save or post_delete
    delete = kwargs.get("created") is None

    if instance:
        # if the compound is paired, update the substance record it's paired to
        if hasattr(instance, "substance"):
            SubstanceIndex().sync_instances(instance.substance, delete)
        # else (the compound is solo) update it's solo record.
        else:
            CompoundIndex().sync_instances(instance, delete)
