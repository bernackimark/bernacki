from ._anvil_designer import PostCardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PostCard(PostCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_like_click(self, **event_args):
    self.btn_like.icon = 'fa:thumbs-up' if self.has_user_liked else 'fa:thumbs-o-up'

  def btn_comment_click(self, **event_args):
    self.tb_comment.visible = False if self.tb_comment.visible else True


