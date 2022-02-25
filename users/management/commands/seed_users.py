from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        # get the number from the console
        number = options.get("number")
        seeder = Seed.seeder()
        # 1 -> model, 2 -> number(int), 3 -> customFieldFormatters(dict, default는 None)
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
