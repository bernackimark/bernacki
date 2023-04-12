import anvil.server

@anvil.server.portable_class
class StatusMessage():
    def __init__(self, is_success: bool, msg: str = 'All good'):
        self.is_success = is_success
        self.msg = msg