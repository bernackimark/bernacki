import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media


import pandas as pd
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup as soup
from PIL import Image, ImageDraw
from io import BytesIO

BASE_URL = 'https://www.pdga.com/player/'
PLAYER_IMG_DEFAULT_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'


@anvil.server.callable
def write_dg_event(**kwargs):
    kwargs['year'] = kwargs['end_date'].year  # i appended this on 9/12/23, not sure if it works
    app_tables.dg_events.add_row(id=len(app_tables.dg_events.search())+1, created_ts=datetime.now(), lmt=datetime.now(), **kwargs)


@anvil.server.callable
def write_disc_golfer(pdga_id: int, first_name: str, last_name: str, division: str):
  img_url, _ = get_player_image_url(pdga_id=pdga_id)
  app_tables.dg_players.add_row(pdga_id=pdga_id, first_name=first_name, last_name=last_name, full_name=f'{first_name} {last_name}', division=division, photo_url=img_url)


@anvil.server.callable
def write_new_tourney_name(name: str):
  if not app_tables.dg_tournaments.get(name=name):
    app_tables.dg_tournaments.add_row(name=name)


def get_player_image_url(pdga_id: int) -> (str, bool):
    url = BASE_URL + str(pdga_id)
    r = requests.get(url).content
    s = soup(r, 'html.parser')
  
    try:
        img_url = s.find(rel="gallery-player_photo").find('img').get('src')
        found = True
    except:
        img_url = PLAYER_IMG_DEFAULT_URL
        found = False
  
    return img_url, found


def manipulate_image(image_url) -> Image:
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download image from {image_url}")

    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
    img = img.resize((150, 150), Image.LANCZOS)

    # Create a mask for the circular crop
    mask = Image.new("L", (150, 150), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 150, 150), fill=255)

    # Apply the circular mask to the image
    img = Image.composite(img, Image.new("RGBA", img.size, (255, 255, 255, 0)), mask)

    return img


def convert_photo_url_to_anvil_media(photo_url: str):
    img: Image = manipulate_image(photo_url)
    img.save('/tmp/image.png')
    return anvil.media.from_file('/tmp/image.png', 'image/png')


@anvil.server.background_task
def update_all_dg_player_photos() -> None:
    for r in app_tables.dg_players.search():
        current_online_image, found = get_player_image_url(r['pdga_id'])
        if found:  # if there is no image found, don't update it ... still provides an image for a player who took down an image
            if r['photo_url'] != current_online_image:
                r['photo_url'] = current_online_image
                r['url'] = convert_photo_url_to_anvil_media(r['photo_url'])
                print(f"Updated image for {r['full_name']}")

@anvil.server.callable
def get_dg_data():
    return app_tables.dg_events.search(q.fetch_only('year', 'governing_body', 'designation', 'end_date',
                                                           'created_ts', 'tourney_link',
                                                           mpo_champ_link=q.fetch_only('full_name', 'photo'),
                                                           fpo_champ_link=q.fetch_only('full_name', 'photo')))
