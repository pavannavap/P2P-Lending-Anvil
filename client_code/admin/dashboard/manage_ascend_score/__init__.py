from ._anvil_designer import manage_ascend_scoreTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_ascend_score(manage_ascend_scoreTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_ascend_score.view_ascend_subcategory')


  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_ascend_score.add_subcategory')

  def button_14_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_ascend_score.view_ascend_group')

  def image_4_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_ascend_score.add_subcategory')

  def image_4_copy_10_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_ascend_score.view_ascend_group')

  def image_4_copy_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_ascend_score.view_ascend_subcategory')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')



