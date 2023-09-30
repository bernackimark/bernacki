import anvil.server
from PIL import Image, ImageDraw


@anvil.server.callable
def image_to_media_obj_w_resize(media_obj, h=-1, w=-1):
    img = Image.open(img)
    img = img.convert("RGBA")
    if h != -1 or w != -1:
        img = img.resize((h, w), Image.LANCZOS)
    img.save('/tmp/image.png')
    return anvil.media.from_file('/tmp/image.png', 'image/png')