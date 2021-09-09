import csv

from django.core.management.base import BaseCommand

from home.models import Device, DailyWalk, IntentionalWalk
from home.utils.generators import AccountGenerator, DeviceGenerator

class Command(BaseCommand):
    help = "Import walk data from csv"

    def add_arguments(self, parser):
        parser.add_argument("FILENAME")
        parser.add_argument("-t", "--type", required=True, choices=["daily", "intentional"])

    def handle(self, *args, **options):
        if options["FILENAME"].endswith(".csv"):
            self._import_csv(*args, **options)

    def _import_csv(*args, **options):
        line_counter = 0
        walk_counter = 0
        acct_gen = AccountGenerator()
        dev_gen = DeviceGenerator()

        filename = options["FILENAME"]
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                line_counter += 1
                device_id = row["device_id"]
                try:
                    device = Device.objects.get(device_id=device_id)
                except Device.DoesNotExist:
                    account = next(acct_gen.generate(1))
                    device = next(dev_gen.generate(1, account=account, device_id=device_id))

                if options["type"] == "daily":
                    DailyWalk.objects.get_or_create(
                        date=row["date"],
                        steps=row["steps"],
                        distance=row["distance"],
                        device=device,
                    )
                elif options["type"] == "intentional":
                    IntentionalWalk.objects.get_or_create(
                        event_id=row["event_id"],
                        start=row["start"],
                        end=row["end"],
                        steps=row["steps"],
                        pause_time=row["pause_time"],
                        distance=row["distance"],
                        device=device,
                    )
                else:
                    raise ValueError(f"Don't know what to do with {options['type']}")
                walk_counter += 1

        print(f"Imported {walk_counter} walks from {filename}.")
