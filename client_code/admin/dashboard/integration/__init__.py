from ._anvil_designer import integrationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class integration(integrationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_copy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.integration.credit_bureau_connectivity')

  def button_14_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.integration.KYC_provider_integration')

  def button_11_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.integration.payment_gateway_integration')

  def view_people_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.integration.accounting_software')

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.integration.API_and_webhook')

  def image_4_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.integration.credit_bureau_connectivity')

  def image_4_copy_10_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.integration.KYC_provider_integration')

  def image_4_copy_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.integration.payment_gateway_integration')

  def image_4_copy_5_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.integration.accounting_software')

  def image_4_copy_10_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.integration.API_and_webhook')
