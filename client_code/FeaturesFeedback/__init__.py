from ._anvil_designer import FeaturesFeedbackTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class FeaturesFeedback(FeaturesFeedbackTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_new_bug_click(self, **event_args):
    if not self.dd_report_bug_apps.selected_value or self.ta_bug_description.text in ['', None]:
      alert('Please enter required information')
      return
    if not anvil.users.get_user():
      alert("Please create an account.  I promise it's quick.")
      return
    msg = anvil.server.call_s('write_to_features_feedback', cat='bug', app=self.dd_report_bug_apps.selected_value,
                        user=anvil.users.get_user(), screenshot=self.fl_bug_screenshot.file, desc=self.ta_bug_description.text)
    Notification(msg)

  def btn_new_request_click(self, **event_args):

    # add the guard clauses here
    
    app = self.dd_new_feature_apps.selected_value if self.rb_existing_app.selected else None
    screenshot = self.fl_bug_screenshot.file if self.fl_bug_screenshot.file else None
    anvil.server.call_s('write_to_features_feedback', cat='feature', app=app,
                        user=anvil.users.get_user(), screenshot=self.fl_bug_screenshot.file, desc=self.ta_bug_description.text)


