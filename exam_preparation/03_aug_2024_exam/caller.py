import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, F, Avg, Sum


# Task 04.
def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)).order_by('name')

    if astronauts is None:
        return ''

    result = []

    for a in astronauts:
        result.append(
            f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {"Active" if a.is_active else "Inactive"}')

    return '\n'.join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if top_astronaut is None or top_astronaut.mission_count == 0 or not top_astronaut.mission_count:
        return 'No data.'

    return f'Top Astronaut: {top_astronaut.name} with {top_astronaut.mission_count} missions.'


def get_top_commander():
    top_commander = Astronaut.objects.annotate(num_of_commanded_missions=Count('commanded_missions')) \
        .order_by('-num_of_commanded_missions', 'phone_number').first()

    if top_commander is None or top_commander.num_of_commanded_missions == 0 or not top_commander.num_of_commanded_missions:
        return 'No data.'

    return f"Top Commander: {top_commander.name} with {top_commander.num_of_commanded_missions} commanded missions."


# Task 05.

def get_last_completed_mission():
    mission = Mission.objects\
        .filter(status='Completed')\
        .order_by('-launch_date').first()

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else "TBA"
    astronauts = mission.astronauts.all().order_by('name')
    astronaut_names = ", ".join(astronaut.name for astronaut in astronauts)
    spacecraft_name = mission.spacecraft.name
    total_spacewalks = astronauts.aggregate(total=Sum('spacewalks'))['total']

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. "
            f"Spacecraft: {spacecraft_name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects \
        .annotate(num_missions=Count('used_in_missions', distinct=True)) \
        .annotate(num_astronauts=Count('used_in_missions__astronauts', distinct=True)) \
        .order_by('-num_missions', 'name') \
        .first()

    if not spacecraft or spacecraft.num_missions == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, "
            f"astronauts on missions: {spacecraft.num_astronauts}.")


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        used_in_missions__status='Planned',
        weight__gte=200.0
    ).distinct()

    if not spacecrafts:
        return "No changes in weight."

    num_spacecrafts_affected = spacecrafts.update(weight=F('weight') - 200.0)
    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {num_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")