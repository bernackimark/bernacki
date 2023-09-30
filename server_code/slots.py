import anvil.server
from PIL import Image, ImageDraw
from io import BytesIO

@anvil.server.callable
def resize_media_obj_image(media_obj, h=-1, w=-1):
    bytes_io = BytesIO(media_obj.get_bytes())
    img = Image.open(bytes_io)
    img = img.convert("RGBA")
    if h != -1 or w != -1:
        img = img.resize((h, w), Image.LANCZOS)
    img.save('/tmp/image.png')
    return anvil.media.from_file('/tmp/image.png', 'image/png')