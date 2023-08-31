import anvil.server
import anvil.email
from bs4 import BeautifulSoup as bs
import requests
from datetime import date, timedelta
from dataclasses import dataclass, field


FG_STANDINGS_HEADERS = ['team_name', 'ytd_g', 'ytd_w', 'ytd_l', 'ytd_pct', 'ytd_run_diff', 'ytd_rs', 'ytd_ra',
                        'ros_g', 'ros_w', 'ros_l', 'ros_pct', 'ros_run_diff', 'ros_rs', 'ros_ra',
                        'proj_w', 'proj_l', 'proj_pct', 'proj_rdiff', 'proj_rs', 'proj_ra']
SUBJECT_COLUMNS = ['team_name', 'ytd_w', 'ytd_l', 'proj_w', 'proj_l']
GAMES_IN_SEASON = 162

yesterday = date.today() - timedelta(1)


@dataclass
class Team:
    name: str
    full_name: str
    code: str
    wins: int = field(init=False)
    losses: int = field(init=False)
    yesterday_result: str = field(init=False)

    @property
    def games_played(self) -> int:
        return self.wins + self.losses

    @property
    def games_remaining(self) -> int:
        return GAMES_IN_SEASON - self.wins - self.losses


@dataclass
class OU:
    team: Team
    adverse: str
    position: str
    cnt: float
    amt: int

    @property
    def amt_dollars(self) -> str:
        return f'${round(self.amt/100)}'

    @property
    def magic_number(self) -> int:
        num = round(self.cnt - self.team.wins) if self.position == 'o' else round(GAMES_IN_SEASON - self.cnt - self.team.losses)
        return num

    @property
    def anti_magic_number(self) -> int:
        return self.team.games_remaining - self.magic_number

    @property
    def outcome(self) -> str:
        if self.magic_number <= 0:
            return 'winner'
        elif self.magic_number > self.team.games_remaining:
            return 'loser'
        else:
            return 'active'

    @property
    def was_yesterday_good(self) -> bool:
        if (self.team.yesterday_result == 'win' and self.position == 'o') or \
           (self.team.yesterday_result == 'loss' and self.position == 'u'):
            return True
        return False

    @property
    def exclaim(self) -> str:
        punctuation = '!' if self.was_yesterday_good else '.'
        return punctuation


bets = [OU(Team('Dodgers', 'Los Angeles Dodgers', 'LAD'), 'Vegas', 'u', 96, 5000),
        OU(Team('Pirates', 'Pittsburgh Pirates', 'PIT'), 'Vegas', 'o', 67, 5000),
        OU(Team('Athletics', 'Oakland Athletics', 'OAK'), 'Vegas', 'o', 59, 20000),
        OU(Team('Braves', 'Atlanta Braves', 'ATL'), 'Jake', 'u', 92, 5000),
        OU(Team('Rangers', 'Texas Rangers', 'TEX'), 'Jake', 'o', 79.5, 5000),
        OU(Team('Red Sox', 'Boston Red Sox', 'BOS'), 'Jake', 'o', 76.5, 5000),
        OU(Team('Nationals', 'Washington Nationals', 'WSN'), 'Jake', 'o', 59.5, 5000),
        OU(Team('Athletics', 'Oakland Athletics', 'OAK'), 'Jake', 'o', 58, 5000)]


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
        for idx, data in enumerate(all_td_tags):  # this requires the table's column composition to remain constant
            team_dict[FG_STANDINGS_HEADERS[idx]] = data.string
        standings.append(team_dict)
    return standings


def update_team_records(current_standings: list[dict]) -> None:
    for bet in bets:
        for team in current_standings:
            if bet.team.name == team['team_name']:
                bet.team.wins = int(team['ytd_w'])
                bet.team.losses = int(team['ytd_l'])


def get_yesterday_results_stats_api() -> list[[tuple[str, bool]]]:
    y = date.today() - timedelta(1)
    d: dict = requests.get(f'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={y}&endDate={y}').json()
    all_outcomes = []
    for e in d['dates'][0]['games']:
        is_winner_away, is_winner_home = e['teams']['away'].get('isWinner'), e['teams']['home'].get('isWinner')
        all_outcomes.append((e['teams']['away']['team']['name'], is_winner_away))
        all_outcomes.append((e['teams']['home']['team']['name'], is_winner_home))
    return all_outcomes


def update_teams_yesterday_result(results: list[[tuple[str, bool]]]) -> None:
    for b in bets:
        if b.team.full_name not in [t[0] for t in results]:
            b.team.yesterday_result = 'off'
            continue
        for res in results:
            if b.team.full_name == res[0]:
                b.team.yesterday_result = 'win' if res[1] else 'loss'


def format_text() -> str:
    text_list = [(f'{b.team.name} {b.amt_dollars} {b.adverse} bet. Yest: {b.team.yesterday_result}{b.exclaim}\nMagic # {b.magic_number}; Anti-magic #: {b.anti_magic_number}.', b.outcome) for b in bets]
    active = [b[0] for b in text_list if b[1] == 'active']
    winners = [b[0] for b in text_list if b[1] == 'winner']
    losers = [b[0] for b in text_list if b[1] == 'loser']
    active_text, winner_text, loser_text = '\n'.join(active), '\n'.join(winners), '\n'.join(losers)
    return f'Active Bets:\n{active_text}\n\nWinners:\n{winner_text}\n\nLosers:{loser_text}'


@anvil.server.callable
@anvil.server.background_task
def run_baseball_bets() -> None:
    html_table: list[str] = get_standings_html()
    teams_season_stats: list[dict] = create_standings_from_html(html_table)
    update_team_records(teams_season_stats)
    yesterday_results: list[dict] = get_yesterday_results_stats_api()
    update_teams_yesterday_result(yesterday_results)
    message_body: str = format_text()
    # send_yagmail('bernackimark@gmail.com', 'Baseball Bets', message_body)

    # this line only works in Anvil
    anvil.email.send(from_name = "Bernacki", to = "bernackimark@gmail.com", subject = "Baseball Bets", text = message_body)
