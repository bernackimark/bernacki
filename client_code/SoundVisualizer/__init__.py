from ._anvil_designer import SoundVisualizerTemplate
from anvil import *
import anvil.facebook.auth
import anvil.server

from . import sound_visualizer as sv

import time

class SoundVisualizer(SoundVisualizerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    speeds = [('Slow', 'slow'), ('Medium', 'medium'), ('Fast', 'fast')]
    schemes = ['maroon', 'gold']
    scales = ['major', 'minor']
    scenes = [('Simple Up & Down', 1), ('Simple Side to Side', 2)]
    [self.fp_speed.add_component(Button(text=s[0])) for s in speeds]
    [self.fp_scheme.add_component(Button(text=s)) for s in schemes]
    self.dd_instrument.items = [('Piano', 'piano')]
    self.dd_scale.items = [s for s in scales]

    sv.sv = sv.SoundVisualizer('medium', 'maroon_tones', 'minor_9', 'piano', 1)
    self.widgets = []

    self.timer.interval = 0

  def draw(self):
      self.widgets.clear()

      for p in sv.sv.pieces:
          if sv.sv.piece_shape == 'rect':
              widget = self.canvas.fill_rect(p.x, p.y, p.shape.width, p.shape.height)
          else:
              raise ValueError
          self.widgets.append(widget)

  def run(self):
      # self.timer.interval=0.2
      while True:
        print(f'My state inside the run function is: {sv.sv.state}')
        if sv.sv.state != 'playing':
          self.timer.tick(interval=0)
        else:
          time.sleep(.02)
          self.canvas.clear_rect(0,0,self.canvas.get_width(),self.canvas.get_height())
          self.draw()
          sv.sv.play()          

  def timer_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.canvas.clear_rect(0,0,self.canvas.get_width(),self.canvas.get_height())
    self.draw()
    sv.sv.play()       
  
  def canvas_reset(self, **event_args):
    """This method is called when the canvas is reset and cleared, such as when the window resizes, or the canvas is added to a form."""
    # self.canvas.reset_context()

  def btn_play_click(self, **event_args):
    self.card_settings.visible = False
    self.timer.interval=0.02
    # self.timer_tick()

  def btn_stop_click(self, **event_args):

    # CANNOT GET ANYTHING ELSE TO FIRE ONCE THE ANIMATION HAS STARTED
    
    print('---------------------------')
    self.timer.interval=0
    sv.sv.pause()
    self.card_settings.visible = True

  def canvas_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    print('Mouse up!!!!')
    sv.sv.pause()
    self.timer.interval=0
    self.card_settings.visible = True
    # if sv.sv.state == 'playing':
    #   sv.sv.pause()
    #   print(f'The state is now: {sv.sv.state}')
    #   print('I am trying to pause')
    # # else:
    # #   sv.sv.play() 




