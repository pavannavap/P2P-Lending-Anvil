from ._anvil_designer import behavioural_reportTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class behavioural_report(behavioural_reportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports')

  def button_6_click(self, **event_args):
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.foreclosure')

  def button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.extension')

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.defaulters')

  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.due_date')

  def image_4_mouse_up(self, x, y, button, **event_args):
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.foreclosure')

  def image_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.extension')

  def image_4_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.defaulters')

  def image_6_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.accounting.mis_reports.behavioural_report.due_date')

