import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Task 01.

def create_pet(name: str, species: str):
    Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))


# Task 02.
def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


# Task 03.
def show_all_locations():
    all_locations = Location.objects.all().order_by('-id')
    result = []

    for location in all_locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)


def new_capital():
    new_cap = Location.objects.first()
    new_cap.is_capital = True
    new_cap.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


# Location.objects.create(
#     name='Sofia',
#     region='Sofia Region',
#     population=1329000,
#     description="The capital of Bulgaria and the largest city in the country",
# )
#
# Location.objects.create(
#     name='Plovdiv',
#     region='Plovdiv Region',
#     population=346942,
#     description="The second-largest city in Bulgaria with a rich historical heritage"
#

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


# Task 04.
def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        percentage_off = sum(int(digit) for digit in str(car.year)) / 100  # 2014 => 2 + 0 + 1 + 4 => 7 / 100 => 0.07
        discount = float(car.price) * percentage_off  # 1000 * 0.07 => 70
        car.price_with_discount = float(car.price) - discount  # 1000 - 70 => 930
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


# Car.objects.all().create(
#     model='Mercedes C63 AMG',
#     year=2019,
#     color='white',
#     price=120000.00
# )
#
# Car.objects.all().create(
#     model='Audi Q7 S line',
#     year=2023,
#     color='black',
#     price=183900.00
#)

# apply_discount()
# print(get_recent_cars())


# Task 05.
def show_unfinished_tasks():
    all_tasks = Task.objects.all()
    result = []

    for task in all_tasks:
        if not task.is_finished:
            result.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return '\n'.join(result)


def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    decoded_msg = []

    for char in text:
        new_char = chr((ord(char) - 3))
        decoded_msg.append(new_char)

    Task.objects.filter(title=task_title).update(description=''.join(decoded_msg))


# Task.objects.all().create(
#     title='Simple Task',
#     description='This is a sample task',
#     due_date='2023-10-31',
#     is_finished=False,
# )


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


# Task 06.
def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    even_deluxe_rooms = [str(r) for r in deluxe_rooms if r.id % 2 == 0]

    return "\n".join(even_deluxe_rooms)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')  # id 1, id 2...

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room() -> None:
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room() -> None:
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


# HotelRoom.objects.create(
#     room_number=401,
#     room_type='Standart',
#     capacity=2,
#     amenities='Tv',
#     price_per_night=100.00
# )
#
# HotelRoom.objects.create(
#     room_number=501,
#     room_type='Deluxe',
#     capacity=3,
#     amenities='Wi-Fi',
#     price_per_night=200.00
# )

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)


# Task 7. Characters

def update_characters():
    all_characters = Character.objects.all()

    for character in all_characters:
        if character.class_name == 'Mage':
            character.level += 3
            character.intelligence -= 7
            character.save()

        elif character.class_name == 'Warrior':
            character.hit_points /= 2
            character.dexterity += 4
            character.save()

        else:
            character.inventory.update('The inventory is empty')


def fuse_characters(first_character: Character, second_character: Character):
    # create a new char
    name = f'{first_character.name} {second_character.name}'
    class_name = 'Fusion'
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ("Mage", "Scout"):
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory

    )
    # delete the current_chars
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()
