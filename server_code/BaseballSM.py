import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from bs4 import BeautifulSoup as bs
import requests
from datetime import date, timedelta
from emailer import send_email


FG_STANDINGS_HEADERS = ['team_name', 'ytd_g', 'ytd_w', 'ytd_l', 'ytd_pct', 'ytd_run_diff', 'ytd_rs', 'ytd_ra',
                        'ros_g', 'ros_w', 'ros_l', 'ros_pct', 'ros_run_diff', 'ros_rs', 'ros_ra',
                        'proj_w', 'proj_l', 'proj_pct', 'proj_rdiff', 'proj_rs', 'proj_ra']
SUBJECT_TEAMS = ['Braves', 'Rangers', 'Red Sox', 'Nationals', 'Athletics', 'Dodgers', 'Pirates']
TEAM_NAME_ABBREVS = [('Dodgers', 'LAD'), ('Pirates', 'PIT'), ('Athletics', 'OAK'), ('Braves', 'ATL'),
                     ('Rangers', 'TEX'), ('Red Sox', 'BOS'), ('Nationals', 'WSN')]
NICKNAME_FULL_NAME = [('Dodgers', 'Los Angeles Dodgers'), ('Pirates', 'Pittsburgh Pirates'),
                      ('Athletics', 'Oakland Athletics'), ('Braves', 'Atlanta Braves'),
                      ('Rangers', 'Texas Rangers'), ('Red Sox', 'Boston Red Sox'), ('Nationals', 'Washington Nationals')]
SUBJECT_COLUMNS = ['team_name', 'ytd_w', 'ytd_l', 'proj_w', 'proj_l']
GAMES_IN_SEASON = 162

yesterday = date.today() - timedelta(1)

bets = [{'team_name': 'Dodgers', 'position': 'under', 'cnt': 96, 'amt': 5000},
        {'team_name': 'Pirates', 'position': 'over', 'cnt': 67, 'amt': 5000},
        {'team_name': 'Athletics', 'position': 'over', 'cnt': 59, 'amt': 20000},
        {'team_name': 'Braves', 'position': 'under', 'cnt': 92, 'amt': 5000},
        {'team_name': 'Rangers', 'position': 'over', 'cnt': 79.5, 'amt': 5000},
        {'team_name': 'Red Sox', 'position': 'over', 'cnt': 76.5, 'amt': 5000},
        {'team_name': 'Nationals', 'position': 'over', 'cnt': 59.5, 'amt': 5000},
        {'team_name': 'Athletics', 'position': 'under', 'cnt': 58, 'amt': 5000}]


def get_standings_html() -> list[str]:
    r = requests.get('https://www.fangraphs.com/depthcharts.aspx?position=Standings')
    s = bs(r.content, 'html.parser')
    return s.find_all(class_='depth_team')


def create_standings_from_html(html_table: list[str]) -> list[dict]:
    standings: list[dict] = []
    for i, row in enumerate(html_table):
        if i > 29:
            continue
        team_dict = dict()
        all_td_tags = row.find_all('td')
        for idx, data in enumerate(all_td_tags):
            team_dict[FG_STANDINGS_HEADERS[idx]] = data.string
        standings.append(team_dict)
    return standings


def filter_teams(all_teams: list[dict], my_teams: list[str]) -> list[dict]:
    return [team for team in all_teams if team['team_name'] in my_teams]


def filter_columns(current: list[dict]) -> list[dict]:
    for d in current:
        key_copy = list(d.keys())
        for k in key_copy:
            if k not in SUBJECT_COLUMNS:
                del d[k]
    return current


def current_bet_stats(fg_teams: list[dict], my_bets: list[dict]) -> list[dict]:
    current_stats: list[dict] = []
    for b in my_bets:
        for fg in fg_teams:
            if b['team_name'] == fg['team_name']:
                remaining_games = GAMES_IN_SEASON - int(fg['ytd_w']) - int(fg['ytd_l'])
                remaining_wins_needed = b['cnt'] - int(fg['ytd_w'])
                play_like_a = int(round((remaining_wins_needed / remaining_games) * 162, 0))
                current_stats.append({'team_name': b['team_name'], 'wins_needed': remaining_wins_needed,
                                      'remaining_games': remaining_games, 'must_play_like': play_like_a})
    return current_stats


def get_yesterday_results_stats_api() -> list[dict]:
    y = date.today() - timedelta(1)
    d: dict = requests.get(f'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={y}&endDate={y}').json()
    all_outcomes = []
    for e in d['dates'][0]['games']:
        all_outcomes.append((e['teams']['away']['team']['name'], e['teams']['away']['isWinner']))
        all_outcomes.append((e['teams']['home']['team']['name'], e['teams']['home']['isWinner']))
    my_outcomes: list[dict] = []
    for t in NICKNAME_FULL_NAME:
        if t[1] not in [o[0] for o in all_outcomes]:
            my_outcomes.append({'team_name': t[0], 'yesterday_result': 'Off day yesterday'})
        for o in all_outcomes:
            if t[1] == o[0]:
                if o[1]:
                    my_outcomes.append({'team_name': t[0], 'yesterday_result': 'They won yesterday'})
                else:
                    my_outcomes.append({'team_name': t[0], 'yesterday_result': 'They lost yesterday'})
    return my_outcomes


def format_text(fg_info: list[dict], bets: list[dict], bet_stats: list[dict], yesterday_results: list[dict]) -> str:
    # stitch the four lists into just one
    [bet.update(bet_stats[idx]) for idx, bet in enumerate(bets)]
    [bet.update(fg_team) for bet in bets for fg_team in fg_info if fg_team['team_name'] == bet['team_name']]
    [bet.update(res) for bet in bets for res in yesterday_results if res['team_name'] == bet['team_name']]
    stitched_list = [f"Bet: {b['team_name']} {b['position']} {b['cnt']}. {b['yesterday_result']}. Their rest of the season line is: {b['wins_needed']}-{b['remaining_games'] - b['wins_needed']}. They must play like a {b['must_play_like']} win team." for b in bets]
    return '\n'.join(stitched_list)


@anvil.server.callable
@anvil.server.background_task
def run_baseball_bets() -> None:
    html_table: list[str] = get_standings_html()
    teams: list[dict] = create_standings_from_html(html_table)
    filtered_teams: list[dict] = filter_teams(teams, SUBJECT_TEAMS)
    fg_data: list[dict] = filter_columns(filtered_teams)
    bet_stats: list[dict] = current_bet_stats(fg_data, bets)
    yesterday_results: list[dict] = get_yesterday_results_stats_api()
    message_body: str = format_text(fg_data, bets, bet_stats, yesterday_results)
    send_email(from_name='Bernacki', to='bernackimark@gmail.com', subject='Baseball Bets', text=message_body)
