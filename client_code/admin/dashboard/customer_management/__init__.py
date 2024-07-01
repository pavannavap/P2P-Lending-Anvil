from ._anvil_designer import customer_managementTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class customer_management(customer_managementTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.customer_management.handles_customer_registration')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.customer_management.kyc_verification')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.customer_management.managing_customer_profile')

  def image_1_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.customer_management.handles_customer_registration')

  def image_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.customer_management.kyc_verification')

  def image_3_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.customer_management.managing_customer_profile')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

  

  
