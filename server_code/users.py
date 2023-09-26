import anvil.facebook.auth
import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

@anvil.server.callable(require_user=True)
def update_handle_and_avatar(handle, avatar):
    row = anvil.users.get_user()
    row['handle'] = handle

    if avatar:
        img = manipulate_image(avatar)
        media_object = anvil.BlobMedia('image/png', avatar, name='avatar.png')
        with anvil.media.TempFile(media_object) as file:
            row['avatar'] = file

    # NEED TO TEST THE ABOVE
        
    # right now the only thing that's required is the handle, this could different in the future
    row['is_confirmed'] = True


def manipulate_image(image) -> Image:
    img = Image.open(image).convert("RGBA").resize((150, 150), Image.LANCZOS)

    # Create a mask for the circular crop
    mask = Image.new("L", (150, 150), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 150, 150), fill=255)

    # Apply the circular mask to the image
    img = Image.composite(img, Image.new("RGBA", img.size, (255, 255, 255, 0)), mask)

    return img