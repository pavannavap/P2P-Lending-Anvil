from ._anvil_designer import eod_reportsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class eod_reports(eod_reportsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    anvil.server.call('update_eod_report')
        # Call your custom method to display today's reports
    self.display_todays_reports()

  def display_todays_reports(self):
        # Get today's date without time (date only)
        today_date = datetime.now().date()
        
        # Retrieve today's report from fin_eod_reports table
        todays_reports = app_tables.fin_eod_reports.search(date=today_date)
        
        # Bind the reports to the repeating panel
        self.repeating_panel_1.items = todays_reports

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports')
