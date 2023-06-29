import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import requests
from bs4 import BeautifulSoup as soup
# not using soup currently, can it help?
# there's also this pre-existing package: https://pypi.org/project/fangraphs/#Leaders with a built-in :
# from fangraph.leaders import leaders
# leaders.MajorLeague()

@anvil.server.callable
def get_fangraphs_leaderboard() -> str:
  res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=20&type=1&season=2023&month=1000&season1=2023&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=2023-05-16&enddate=2023-12-31&sort=21,a')
  return res.text

@anvil.server.callable
def get_fangraphs_standings() -> str:
  r = requests.get('https://www.fangraphs.com/depthcharts.aspx?position=Standings')
  s = soup(r.content)
  standings = s.find_all(class_='depth_team')
  return standings