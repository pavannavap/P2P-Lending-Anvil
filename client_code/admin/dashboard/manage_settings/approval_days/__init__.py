from ._anvil_designer import approval_daysTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class approval_days(approval_daysTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.current_entry_id = None
    self.current_default_entry_id = None
    self.display_latest_settings()

  def is_valid_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

  def save_button(self, **event_args):
    # Get the values from the text boxes
    value1 = self.text_box_1.text
    value2 = self.text_box_2.text
    if self.is_valid_int(value1) and self.is_valid_int(value2):
       value1 = int(value1)
       value2 = int(value2)
       if self.current_entry_id:
                # Update the existing entry
                entry = app_tables.fin_approval_days.get(loans='Extension')
                entry.update(
                    days_for_approval=value1,
                )
       else:
                # Insert new values into the fin_loan_settings table
                entry = app_tables.fin_approval_days.add_row(
                    days_for_approval=value1,
                    loans="Extension"
                )
                self.current_entry_id = entry.get_id()

       if self.current_default_entry_id:
                # Update the existing default fee entry
                default_entry = app_tables.fin_approval_days.get(loans='Foreclosure')
                if default_entry:
                    default_entry.update(
                        days_for_approval=value2,
                    )
       else:
                # Insert new default fee values into the fin_loan_settings table
                default_entry = app_tables.fin_approval_days.add_row(
                    days_for_approval=value2,
                    loans="Foreclosure"
                )
                self.current_default_entry_id = default_entry.get_id()

       self.display_latest_settings()
       alert("Loan days saved successfully!")
    else:
            alert("Please enter valid integer values for all fields.")

  def display_latest_settings(self):
        """Fetch and display the latest loan settings based on 'lapsed fee'"""
        # Fetch the entry with loans set to 'lapsed fee' from the fin_loan_settings table
        latest_entry = app_tables.fin_approval_days.get(loans="Extension")
        if latest_entry:
            self.current_entry_id = latest_entry.get_id()
            self.text_box_1.text = latest_entry['days_for_approval']
            self.text_box_1.enabled = False
        else:
            self.current_entry_id = None
            self.text_box_1.text = ""
            self.text_box_1.enabled = True

        default_entry = app_tables.fin_approval_days.get(loans="Foreclosure")
        if default_entry:
            self.current_default_entry_id = default_entry.get_id()
            self.text_box_2.text = default_entry['days_for_approval']
            self.text_box_2.enabled = False
        else:
            self.current_default_entry_id = None
            self.text_box_2.text = ""
            self.text_box_2.enabled = True

  def edit_button(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_1.enabled = True
    self.text_box_2.enabled = True

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings')
