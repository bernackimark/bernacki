from ._anvil_designer import PostCommentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PostComment(PostCommentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.img_avatar.source = self.item['avatar']
    self.lbl_handle.text = self.item['handle']
    self.lbl_text.text = self.item['text']
    self.lbl_time_ago.text = self.item['time_ago']
    