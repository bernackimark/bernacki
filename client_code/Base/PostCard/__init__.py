from ._anvil_designer import PostCardTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PostCard(PostCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    self.img_user.source = self.item['avatar']
    self.lbl_handle.text = self.item['handle']
    self.lbl_time_ago.text = self.item['time_ago']
    self.lbl_body.text = self.item['body']
    # self.img_body.source = ???
    self.lbl_like_cnt.text = self.item['like_cnt']
    self.link_comments.text = f"{self.item['comment_cnt']} {'comment' if self.item['comment_cnt'] == 1 else 'comments'}"
    self.has_user_liked = self.item['has_user_liked']
    self.lbl_liked.icon = 'fa:thumbs-up' if self.has_user_liked else 'fa:thumbs-o-up'
    self.lbl_title.text = self.item['title']
    self.rp_comments.items = [c for c in self.item['comments']]

  def btn_like_click(self, **event_args):

    # this needs to send data to the back-end
    
    if not self.has_user_liked:
      self.has_user_liked = True
      self.lbl_liked.icon = 'fa:thumbs-up'
    else:
      self.has_user_liked = False
      self.lbl_liked.icon = 'fa:thumbs-o-up'

  def btn_comment_click(self, **event_args):
    self.cp_create_comment.visible = False if self.cp_create_comment.visible else True

  def link_comments_click(self, **event_args):
    self.cp_create_comment.visible = False if self.cp_create_comment.visible else True

