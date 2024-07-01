from ._anvil_designer import notificationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class notification(notificationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.dasboard_about")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.dasboard_contact")

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def wallet_dashboard_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wallet.wallet')

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard')
