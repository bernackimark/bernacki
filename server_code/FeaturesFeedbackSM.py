import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import uuid
from enum import Enum

class RequestStatuses(Enum):
  REPORTED = 'reported'
  IN_PROCESS = 'in-process'
  COMPLETED = 'completed'
  REJECTED = 'rejected'

FF_NEW_STATUS = RequestStatuses.REPORTED.value

# require_user can take a boolean or a function.  if given a function, that function will receive the currently logged in user (the return value of anvil.users.get_user())
@anvil.server.callable(require_user=True)
def write_to_features_feedback(cat: str, app: str, user: dict, status: str, screenshot: str, desc: str) -> str:
  print(user)
  submitter_name = f"{user['first_name']} {user['last_name']}"
  app_tables.bugs_features.add_row(id=uuid.uuid4(), category=cat, app=app,
                                   submitter_email=user['email'], submitter_name=submitter_name, status=FF_NEW_STATUS, screenshot=screenshot, description=desc)
  return 'I logged your submission.  Thank you!!'


@anvil.server.callable(require_user=True)
def get_all_requests() -> list[dict]:
  return [r for r in app_tables.bugs_features.search() if r['status'] != RequestStatuses.REJECTED.value]
  