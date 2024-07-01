from ._anvil_designer import manage_credit_limitTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re


class manage_credit_limit(manage_credit_limitTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.text_box_1.enabled = False
        # Set event handlers
        self.edit_button.set_event_handler('click', self.edit_button_click)
        self.save_button.set_event_handler('click', self.save_button_click)
        # self.text_box_1.set_event_handler('change', self.text_box_1_change)
        
    def edit_button_click(self, **event_args):
        """This method is called when the edit button is clicked."""
        self.text_box_1.enabled = True

    # def text_box_1_change(self, **event_args):
    #     """This method is called when the text in the text box is changed."""
    #     value = self.text_box_1.text
    #     # Remove spaces from the text
    #     if ' ' in value:
    #         # value = value.replace(' ', '')
    #         # self.text_box_1.text = value
    #         # hex = self.text_box_1.text
    #         alert("Spaces are not allowed in the input")
    #         return

      
    def save_button_click(self, **event_args):
        """This method is called when the save button is clicked."""
        
        value = self.text_box_1.text  # Strip leading and trailing spaces
        if not value.isdigit():
            alert("Value must be a valid number without spaces or alphabets.")
            return
        # Convert to numeric value if needed
        numeric_value = int(value)
        
        # Call server function to save data
        anvil.server.call('save_credit_limit', numeric_value)
      
        # Disable text box after saving
        self.text_box_1.enabled = False
        alert("Data saved successfully!")

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.manage_settings')
    
   