from ._anvil_designer import GuessLogRowTemplate
from anvil import *
import anvil.server

class GuessLogRow(GuessLogRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
      
    for idx, c in enumerate(self.item['guess']):
      image = Image(source=c.image, height=50, display_mode='shrink_to_fit')
      # using a grid panel because i couldn't get the images to appear on a flow panel.  not sure why.
      link = Link()
      link.add_component(image)
      self.gp_guess_log_row_colors.add_component(link, row='A', col_xs=idx*2, width_xs=2)  
