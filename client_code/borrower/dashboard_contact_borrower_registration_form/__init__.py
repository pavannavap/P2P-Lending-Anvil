from ._anvil_designer import dashboard_contact_borrower_registration_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class dashboard_contact_borrower_registration_form(dashboard_contact_borrower_registration_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("borrower.dashboard")

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Logged out sucessfully")
    anvil.users.logout()
    open_form('bank_users.main_form')


  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.borrower_dashboard_about')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard.notification')

  def wallet_dashboard_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wallet.wallet')


