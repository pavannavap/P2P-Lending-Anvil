from ._anvil_designer import home_button_adminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class home_button_admin(home_button_adminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    open_form('admin.dashboard')

  def Admins_click(self, **event_args):
    open_form('admin.dashboard.admin_management')

  def Borrowers_click(self, **event_args):
    open_form('admin.dashboard.borrowers')

  def Lenders_click(self, **event_args):
    open_form('admin.dashboard.lenders')

  def Management_click(self, **event_args):
    open_form('admin.dashboard.loan_management')

  def Products_click(self, **event_args):
    open_form('admin.dashboard.manage_products')

  def CMS_click(self, **event_args):
    open_form('admin.dashboard.manage_cms')

  def ascend_click(self, **event_args):
    open_form('admin.dashboard.manage_ascend')

  def Settings_click(self, **event_args):
    open_form('admin.dashboard.manage_settings')

  def logout__click(self, **event_args):
    anvil.users.logout()
    open_form('bank_users.main_form')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

