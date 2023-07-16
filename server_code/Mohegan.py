import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from emailer import send_email
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dataclasses import dataclass

import time
driver = webdriver.Chrome()
driver.implicitly_wait(4)
wait = WebDriverWait(driver, 10)

LOGIN_URL = 'https://mohegansun.com/login.html'
USERNAME = 'codewordz1'
PASSWORD = 'October2006'
MONTH_COUNT = 2
CURRENT_NIGHTLY_FEES = 45
DOLLAR_THRESHOLD = 200
EXCLUDED_DOWS = ['Tuesday']


@dataclass
class Night:
    date_str: str
    base_dollars: int

    @property
    def price(self) -> int:
        return self.base_dollars + CURRENT_NIGHTLY_FEES

    @property
    def dow(self):
        return self.date_str.split(',')[0]

    @property
    def dow_and_date(self):
        dad_list = self.date_str.split(',')[0:2]
        return f'{dad_list[0]},{dad_list[1]}'


def login(url=LOGIN_URL):
    # login screen
    driver.get(url)
    driver.find_element(By.CLASS_NAME, 'openid-submit-btn').click()
    # enter username screen
    e = driver.find_element(By.NAME, 'identifier')
    e.click()
    e.send_keys(USERNAME)
    e.submit()
    # how do you want to receive your password?
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'sty-radio')
    # the 3rd radio button is sending a magic link to my cell
    e = radio_buttons[3]
    e.click()
    e.submit()
    # magic link is sent to cell
    wait.until(ec.presence_of_element_located((By.NAME, 'password')))
    # password screen
    e = driver.find_element(By.NAME, 'password')
    e.click()
    e.send_keys(PASSWORD)
    e.submit()


def navigate_to_calendar():
    # click Book A Stay
    e = driver.find_element(By.CLASS_NAME, 'bookVisitLink')
    e.click()


def get_rates(html) -> list[Night]:
    soup = BeautifulSoup(html, 'html.parser')
    nights = []
    for day in soup.find_all(class_='selectable-date'):
        day_text: str = day.attrs['title'].replace('Select ', '')
        price: int = int(day.find(class_='calendar-day-data').text.replace('$', ''))
        nights.append(Night(day_text, price))
    return nights


def navigate_to_next_month():
    driver.find_element(By.CLASS_NAME, 'datepick-cmd-next').click()
    time.sleep(5)  # just in case


def filter_nights(nights: list[Night]) -> list[Night]:
    return [n for n in nights if n.price <= DOLLAR_THRESHOLD and n.dow not in EXCLUDED_DOWS]


def create_message_text(night_list: list[Night]) -> str:
    text = ''
    for n in night_list:
        text += f'{n.dow_and_date}, ${n.price}\n'
    return text


@anvil.server.callable
@anvil.server.background_task
def run_mohegan_scrape():
    login(LOGIN_URL)
    navigate_to_calendar()
    time.sleep(10)
    rates: list[Night] = []
    for i in range(MONTH_COUNT + 1):
        rates.extend(get_rates(driver.page_source))
        if i <= MONTH_COUNT:
            navigate_to_next_month()
    driver.close()
    filtered: list[Night] = filter_nights(rates)
    email_text: str = create_message_text(filtered)
    send_email(from_name='Bernacki', to='bernackimark@gmail.com', subject='Mohegan Rates', text=email_text)


