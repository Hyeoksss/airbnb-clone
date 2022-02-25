import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates rooms"

    # 인자 전달
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    # 실질적인 역할 수행
    def handle(self, *args, **options):
        # get number from console
        number = options.get("number")
        # 데이터를 seed하기 위한 사전준비
        seeder = Seed.seeder()
        # seeder는 foriegn key를 활용할 수 없다
        # 하지만 데이터가 클 경우는 다른 방법을 써야 함
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
            },
        )
        # seeder.execute를 통해 room-data를 만들고 그것을 created_rooms에 저장
        created_rooms = seeder.execute()
        # flatten을 통해 id(primary key)값을 얻는다
        # 왜 primary key가 1부터 시작안하고 272부터 시작할까?
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                pick_num = random.randint(0, 15)
                if pick_num % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                pick_num = random.randint(0, 15)
                if pick_num % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                pick_num = random.randint(0, 15)
                if pick_num % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
