import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

from PIL import Image, ImageDraw
import io

@anvil.server.callable(require_user=True)
def update_handle_and_avatar(handle, avatar):
    row = anvil.users.get_user()
    row['handle'] = handle

    if avatar:
        img = create_circle_cropped_image(avatar)
        row['avatar'] = img_to_media_obj(img)

    # NEED TO TEST THE ABOVE
        
    # right now the only thing that's required is the handle, this could different in the future
    row['is_confirmed'] = True


def create_circle_cropped_image(media_object, diameter: int = 150) -> Image:
    with anvil.media.TempFile(media_object) as file:
        img = Image.open(file).convert("RGBA").resize((diameter, diameter), Image.LANCZOS)
    
        # Create a mask for the circular crop
        mask = Image.new("L", (diameter, diameter), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, diameter, diameter), fill=255)
    
        # Apply the circular mask to the image
        img = Image.composite(img, Image.new("RGBA", img.size, (255, 255, 255, 0)), mask)
    
        return img


def img_to_media_obj(img):
    img.save('/tmp/image.png')
    return anvil.media.from_file('/tmp/image.png', 'image/png')