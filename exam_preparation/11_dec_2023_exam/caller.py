import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Count


# Create and run your queries within functions

# Task 04.
# Score: 66/75
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    players = None

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name, country__icontains=search_country)
    else:
        if search_name is not None:
            players = TennisPlayer.objects.filter(full_name__icontains=search_name)
        elif search_country is not None:
            players = TennisPlayer.objects.filter(country__icontains=search_country)

    if not players:
        return ''

    players.order_by('ranking')

    result = []

    for p in players:
        result.append(f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}')

    return '\n'.join(result)

def get_top_tennis_player():
    top_tennis_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not top_tennis_player:
        return ''

    return f'Top Tennis Player: {top_tennis_player.full_name} with {top_tennis_player.wins_count} wins.'




# The problem is in this func
def get_tennis_player_by_matches_count():
    player_with_most_matches = TennisPlayer.objects \
        .annotate(num_matches=Count('matches')) \
        .order_by('-num_matches', 'ranking') \
        .first()

    if player_with_most_matches and player_with_most_matches.num_matches > 0:
        return f"Tennis Player: {player_with_most_matches.full_name} with {player_with_most_matches.num_matches} matches played."
    return ""



# Task 05.
def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments_with_this_surface = Tournament.objects.annotate(
        num_matches=Count('matches')
    ).filter(surface_type__icontains=surface).order_by('-start_date')

    if tournaments_with_this_surface is None:
        return ''

    result = []
    for t in tournaments_with_this_surface:
        result.append(f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}')

    return '\n'.join(result)


def get_latest_match_info():
    latest_match = Match.objects.order_by('-date_played').first()

    if not latest_match:
        return ''

    players = [player.full_name for player in latest_match.players.order_by('full_name')]

    return (f"Latest match played on: {latest_match.date_played},"
            f" tournament: {latest_match.tournament.name},"
            f" score: {latest_match.score},"
            f" players: {' vs '.join(players)},"
            f" winner: {latest_match.winner.full_name if latest_match.winner else 'TBA'},"
            f" summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return 'No matches found.'

    matches_by_tournament = Match.objects.filter(tournament__name__exact=tournament_name).order_by('-date_played', '-id') # tournament and id

    if not matches_by_tournament:
        return 'No matches found.'

    result = []

    for m in matches_by_tournament:
        result.append(
            f'Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else "TBA"}')

    return '\n'.join(result)
