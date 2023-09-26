from ._anvil_designer import FeaturesFeedbackTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..user import user

class FeaturesFeedback(FeaturesFeedbackTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    m.my_apps = m.MyApps()
    
    self.dd_new_feature_apps.items = self.dd_report_bug_apps.items = [(a['title'], a['name']) for a in user.my_apps]
    self.tb_bug_title.placeholder, self.tb_feature_title.placeholder = 'My issue title', 'My feature/idea title'
    self.ta_bug_description.placeholder = self.ta_new_description.placeholder = 'My description.  Please enter as much information as possible.'
    
    if user.logged_in:
      self.card_feature_requests.visible = True
      self.lbl_log_in_to_see_feature_requests.visible = False
      self.get_existing_requests()
    else:
      self.card_feature_requests.visible = False
      self.lbl_log_in_to_see_feature_requests.visible = True   

  def btn_new_bug_click(self, **event_args):
    if not self.dd_report_bug_apps.selected_value or self.ta_bug_description.text in ['', None]:
      alert('Please enter required information')
      return
    if len(self.ta_bug_description.text) < 10:
      alert('Please provide a fuller description.')
      return
    msg = anvil.server.call('write_to_features_feedback', cat='bug', app=self.dd_report_bug_apps.selected_value,
                        user=user, screenshot=self.fl_bug_screenshot.file, title=self.tb_bug_title.text, desc=self.ta_bug_description.text)
    if self.fl_bug_screenshot.file:
      self.fl_bug_screenshot.clear()
    Notification(msg).show()

  def btn_new_request_click(self, **event_args):
    if not user.logged_in:
      alert("Please create an account.  I promise it's quick.")
      return
    if not self.rb_existing_app.get_group_value():
      alert('Please select whether your request is on an existing app or is a completely new idea.')
      return
    if self.rb_existing_app.get_group_value() == 'existing_app' and self.dd_new_feature_apps.selected_value in ['', None]:
      alert('Please select the app that your feature is regarding.')
      return
    if self.ta_new_description.text in ['', None] or len(self.ta_new_description.text) < 10:
      alert('Please provide a fuller description.')
      return
    
    app = self.dd_new_feature_apps.selected_value if self.rb_existing_app.selected else None
    screenshot = self.fl_bug_screenshot.file if self.fl_bug_screenshot.file else None
    cat = 'enhancement' if self.rb_existing_app.selected else 'new'
    msg = anvil.server.call('write_to_features_feedback', cat=cat, app=app,
                        user=user, title=self.tb_feature_title.text, desc=self.ta_new_description.text)
    self.get_existing_requests()
    Notification(msg).show()
    
  def get_existing_requests(self):
    self.rp_feature_requests.items = anvil.server.call_s('get_feature_requests', user)

  def dd_new_feature_apps_change(self, **event_args):
    self.rb_existing_app.selected = True

