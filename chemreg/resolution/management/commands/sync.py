from django.apps import apps
from django.core.management import BaseCommand

import requests

from chemreg.resolution.indices import CompoundIndex, SubstanceIndex


class Command(BaseCommand):
    help = "Syncs chemcurator models with resolver"

    def handle(self, *args, **options):
        # I'm stealing the migrate heading because it looks good.
        self.stdout.write(
            self.style.MIGRATE_HEADING("Syncing Substances with Resolver")
        )

        substance_index = SubstanceIndex(fail_silently=False)

        try:
            self.clear_instances(substance_index)
            self.sync_substances(substance_index)
            self.sync_compounds()
        except requests.exceptions.ConnectionError as conn_err:
            self.stderr.write(str(conn_err))
        except Exception as e:
            self.stderr.write(str(e))
        else:
            self.stdout.write(self.style.SUCCESS("Substances Synced"))

    def clear_instances(self, substance_index):
        # Delete existing index
        self.stdout.write("Clearing index... ")
        substance_index.delete_all_instances()
        self.stdout.write(self.style.SUCCESS("Done"))

    def sync_substances(self, substance_index):
        # Loop through all substances and post.
        sub_count = apps.get_model("substance.Substance").objects.count()
        self.stdout.write(f"Updating {sub_count} substances... ")

        substance_index.sync_instances(
            apps.get_model("substance.Substance").objects.all()
        )

        self.stdout.write(self.style.SUCCESS("Done"))

    def sync_compounds(self):
        compound_index = CompoundIndex(fail_silently=False)

        qs = apps.get_model("compound.BaseCompound").objects.filter(
            substance__isnull=True
        )

        # Loop through all compounds not associated with a substance and post.
        comp_count = qs.count()
        self.stdout.write(f"Updating {comp_count} orphan compounds... ")

        compound_index.sync_instances(qs.all())

        self.stdout.write(self.style.SUCCESS("Done"))
