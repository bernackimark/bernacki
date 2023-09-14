import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from . import admin as a

from dataclasses import dataclass, field, asdict
import uuid
from datetime import datetime
from enum import Enum

class BugFeatureCategory(Enum):
  NEW = 'new'
  ENHANCEMENT = 'enhancement'
  BUG = 'bug'

class RequestStatus(Enum):
  REPORTED = 'reported'
  IN_PROCESS = 'in-process'
  COMPLETED = 'completed'
  REJECTED = 'rejected'

@dataclass
class BugFeature:
  category: BugFeatureCategory
  app: str
  submitter_email: str
  submitter_name: str
  description: str
  title: str = None
  screenshot: str = None
  submitted_ts: datetime = datetime.now()
  status: RequestStatus = RequestStatus.REPORTED.value
  is_admin_only: bool = False
  id: str = str(uuid.uuid4())
  history: list = field(default_factory=list)

  def __post_init__(self):
    if not self.title:
      self.title = create_title_from_text(self.description)


def create_title_from_text(text: str) -> str:
  first_period_space_index = text.find('. ')
  if len(text.split(' ')) <= 10:
      return text
  elif first_period_space_index == -1:
      first_ten_words = text.split(' ')[:10]
      return ' '.join(first_ten_words)
  else:
      return text.split('. ')[0] + '.'


@anvil.server.callable
def write_to_features_feedback(cat: str, app: str, user: dict, title: str, desc: str, screenshot: str = None) -> str:
  submitter_name = user['handle'] if user else None
  submitter_email = user['email'] if user else None
  req = BugFeature(category=cat, app=app, submitter_email=submitter_email, submitter_name=submitter_name, title=title, description=desc, screenshot=screenshot)
  d = asdict(req)
  app_tables.bugs_features.add_row(**d)
  return 'I logged your submission.  Thank you!!'


@anvil.server.callable(require_user=True)
def get_feature_requests(user) -> list[dict]:
  if not user['is_admin']:
    my_apps: list[tuple] = a.get_my_apps(user)
    my_app_names = [a[1] for a in my_apps]
    return sorted([r for r in app_tables.bugs_features.search() if r['status'] != RequestStatus.REJECTED.value and not r['is_admin_only'] 
                   and not r['category'] == 'bug' and (not r['app'] or r['app'] in my_app_names)],
                  key = lambda x: x['submitted_ts'], reverse=True)
  return [r for r in app_tables.bugs_features.search() if r['status'] != RequestStatus.REJECTED.value]
  