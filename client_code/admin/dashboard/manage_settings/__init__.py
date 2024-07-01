from ._anvil_designer import manage_settingsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_settings(manage_settingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.dashboard')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.manage_membership')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.manage_ascend_score_range')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.manage_credit_limit')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.manage_facts')

  def image_4_copy_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings.manage_membership')

  def image_1_copy_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings.manage_ascend_score_range')


  def image_1_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings.manage_credit_limit')

  def button_1_manage_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.manage_credit_limit')

  def loan_settings(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.loan_settings')

  def image_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings.loan_settings')

  def image_4_copy_3_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings.approval_days')

  def day_approval(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings.approval_days')

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')
    
