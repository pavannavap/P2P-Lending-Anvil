from ._anvil_designer import add_groupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_group(add_groupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def add_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Get the text entered in the TextBox
        group_name = self.text_box_1.text.strip()  # Trim leading and trailing spaces

        # Check if the group name is not empty
        if group_name:
            # Convert the entered group name to lowercase for case-insensitive comparison
            group_name_lower = group_name.lower()

            # Check if the group name already exists (case-insensitive)
            if any(row['name'].lower() == group_name_lower for row in app_tables.fin_product_group.search()):
                alert(f'Group "{group_name}" already exists. Please choose a different Group name.')
            else:
                # Add a new row only if the group name does not exist
                app_tables.fin_product_group.add_row(name=group_name)
                self.text_box_1.text = ''
                alert(f'Group "{group_name}" added successfully!')
                open_form('admin.dashboard.manage_products.add_product_categories_and_groups')
        else:
            alert("Please enter a group name before saving.")
  
  def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard')

  def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.manage_products.add_product_categories_and_groups')
  # def button_1_copy_2_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   open_form('admin.dashboard.manage_products')

  def button_1_copy_3_click(self, **event_args):
    open_form('admin.dashboard.manage_products.choose_grooup_categoris')
