import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.email

def send_email(from_name: str, to: str, subject: str, text: str):
    anvil.email.send(
      from_name=from_name,
      to=to,
      subject=subject,
      text=text
      # html is another parm if desired
    )