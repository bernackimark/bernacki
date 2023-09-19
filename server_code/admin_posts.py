import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media


@anvil.server.callable(require_user=lambda u: u['is_admin'])
def create_post(title: str, body_text: text, user, media: anvil.media = None):
    pass

    # refer back to testing3 in PyCharm
