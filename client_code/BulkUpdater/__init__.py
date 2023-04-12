from ._anvil_designer import BulkUpdaterTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class BulkUpdater(BulkUpdaterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.task_dd = DropDown(placeholder='What Do You Want To Do?', items=[('', 0), ('Bulk Closure', 1), ('Change Ownership', 2)])
    self.task_dd.add_event_handler('change', self.task_selected)
    self.task_lbl = Label(align='center')
    self.file_uploader = FileLoader(align='center', file_types=['csv','xls','xlsx'], text='Browse for your spreadsheet', multiple=False)
    self.file_uploader.add_event_handler('change', self.file_uploaded)
    self.main_card.add_component(self.task_dd)
    self.main_card.add_component(self.task_lbl)
    self.main_card.add_component(self.file_uploader)
    self.file_uploader.visible = False
  
  def task_selected(self, **event_args):
    if self.task_dd.selected_value == 1:
      self.task_lbl.text = 'Please upload your two-column spreadsheet of item numbers and new statuses.'
      self.file_uploader.visible = True
    elif self.task_dd.selected_value == 2:
      self.task_lbl.text = 'Please upload your two-column spreadsheet of item numbers and new owners.'
      self.file_uploader.visible = True
    else:
      self.task_lbl.text = ''
      self.file_uploader.visible = False

  def file_uploaded(self, file, **event_args):
    self.file_uploader.clear()
    status_message = anvil.server.call('is_data_valid', file, self.task_dd.selected_value)
    alert(status_message.msg)