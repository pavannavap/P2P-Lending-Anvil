from ._anvil_designer import security_and_complianceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class security_and_compliance(security_and_complianceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.security_and_compliance.regulatory_compliance')

  def image_4_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.security_and_compliance.regulatory_compliance')

  def button_14_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.security_and_compliance.Data_Security')

  def button_11_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.security_and_compliance.access_management')

  def image_4_copy_10_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.security_and_compliance.Data_Security')

  def image_4_copy_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.security_and_compliance.')
