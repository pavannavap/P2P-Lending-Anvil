from ._anvil_designer import loan_settingsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class loan_settings(loan_settingsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.current_entry_id = None
        self.current_default_entry_id = None
        self.current_npa_entry_id = None

        # Display the latest loan settings when the form opens.
        self.display_latest_settings()
        # Any code you write here will run before the form opens.
        self.text_box_2.set_event_handler('change', self.update_text_box_3)
        self.text_box_4.set_event_handler('change', self.update_text_box_5)

    def is_valid_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def update_text_box_3(self, **event_args):
        value = self.text_box_2.text
        if value and self.is_valid_int(value):
            next_value = int(value) + 1
            self.text_box_3.text = str(next_value)

    def update_text_box_5(self, **event_args):
        value = self.text_box_4.text
        if value and self.is_valid_int(value):
            next_value = int(value) + 1
            self.text_box_5.text = str(next_value)

    def save_button(self, **event_args):
        """This method is called when the button is clicked"""
        value1 = self.text_box_1.text
        value2 = self.text_box_2.text
        default_value1 = self.text_box_3.text
        default_value2 = self.text_box_4.text
        npa_value1 = self.text_box_5.text
        npa_value2 = self.text_box_6.text

        if self.is_valid_int(value1) and self.is_valid_int(value2) and \
           self.is_valid_int(default_value1) and self.is_valid_int(default_value2) and \
           self.is_valid_int(npa_value1) and self.is_valid_int(npa_value2):
            value1 = int(value1)
            value2 = int(value2)
            default_value1 = int(default_value1)
            default_value2 = int(default_value2)
            npa_value1 = int(npa_value1)
            npa_value2 = int(npa_value2)

            if value1 >= value2:
                alert("Late Payment Minimum Days must be less than Late Payment Maximum Days.")
                return
            if default_value1 >= default_value2:
                alert("default Minimum Days must be less than default Maximum Days.")
                return
            if npa_value1 >= npa_value2:
                alert("NPA Minimum Days must be less than NPA Maximum Days.")
                return

            if self.current_entry_id:
                # Update the existing entry
                entry = app_tables.fin_loan_settings.get(loans='lapsed fee')
                entry.update(
                    minimum_days=value1,
                    maximum_days=value2
                )
            else:
                # Insert new values into the fin_loan_settings table
                entry = app_tables.fin_loan_settings.add_row(
                    minimum_days=value1,
                    maximum_days=value2,
                    loans="lapsed fee"
                )
                self.current_entry_id = entry.get_id()

            if self.current_default_entry_id:
                # Update the existing default fee entry
                default_entry = app_tables.fin_loan_settings.get(loans='default fee')
                if default_entry:
                    default_entry.update(
                        minimum_days=default_value1,
                        maximum_days=default_value2
                    )
            else:
                # Insert new default fee values into the fin_loan_settings table
                default_entry = app_tables.fin_loan_settings.add_row(
                    minimum_days=default_value1,
                    maximum_days=default_value2,
                    loans="default fee"
                )
                self.current_default_entry_id = default_entry.get_id()

            if self.current_npa_entry_id:
                # Update the existing NPA fee entry
                npa_entry = app_tables.fin_loan_settings.get(loans='NPA fee')
                if npa_entry:
                    npa_entry.update(
                        minimum_days=npa_value1,
                        maximum_days=npa_value2
                    )
            else:
                # Insert new NPA fee values into the fin_loan_settings table
                npa_entry = app_tables.fin_loan_settings.add_row(
                    minimum_days=npa_value1,
                    maximum_days=npa_value2,
                    loans="NPA fee"
                )
                self.current_npa_entry_id = npa_entry.get_id()

            # Display the latest settings and make the text boxes non-editable
            self.display_latest_settings()

            # Optionally, display a success message
            alert("Loan days saved successfully!")
        else:
            alert("Please enter valid integer values for all fields.")

    def display_latest_settings(self):
        """Fetch and display the latest loan settings based on 'lapsed fee'"""
        # Fetch the entry with loans set to 'lapsed fee' from the fin_loan_settings table
        latest_entry = app_tables.fin_loan_settings.get(loans="lapsed fee")
        if latest_entry:
            self.current_entry_id = latest_entry.get_id()
            self.text_box_1.text = latest_entry['minimum_days']
            self.text_box_2.text = latest_entry['maximum_days']
            self.text_box_1.enabled = False
            self.text_box_2.enabled = False
        else:
            self.current_entry_id = None
            self.text_box_1.text = ""
            self.text_box_2.text = ""
            self.text_box_1.enabled = True
            self.text_box_2.enabled = True

        default_entry = app_tables.fin_loan_settings.get(loans="default fee")
        if default_entry:
            self.current_default_entry_id = default_entry.get_id()
            self.text_box_3.text = default_entry['minimum_days']
            self.text_box_4.text = default_entry['maximum_days']
            self.text_box_3.enabled = False
            self.text_box_4.enabled = False
        else:
            self.current_default_entry_id = None
            self.text_box_3.text = ""
            self.text_box_4.text = ""
            self.text_box_3.enabled = True
            self.text_box_4.enabled = True

        npa_entry = app_tables.fin_loan_settings.get(loans="NPA fee")
        if npa_entry:
            self.current_npa_entry_id = npa_entry.get_id()
            self.text_box_5.text = npa_entry['minimum_days']
            self.text_box_6.text = npa_entry['maximum_days']
            self.text_box_5.enabled = False
            self.text_box_6.enabled = False
        else:
            self.current_npa_entry_id = None
            self.text_box_5.text = ""
            self.text_box_6.text = ""
            self.text_box_5.enabled = True
            self.text_box_6.enabled = True

    def edit_button(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_1.enabled = True
        self.text_box_2.enabled = True
        self.text_box_3.enabled = True
        self.text_box_4.enabled = True
        self.text_box_5.enabled = True
        self.text_box_6.enabled = True

    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.manage_settings')
