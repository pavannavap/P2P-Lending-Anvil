from ._anvil_designer import edit_other_loanTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class edit_other_loan(edit_other_loanTemplate):
  def __init__(self, selected_row, **properties):
    self.init_components(**properties)

    # Set the initial values for the input components
    self.text_box_1.text = selected_row['sub_category']
    self.text_box_1.enabled = False

    self.text_box_2.text = selected_row['min_points']
    self.text_box_2.enabled = True

    self.selected_row = selected_row

  def save_click(self, **event_args):
    """Save changes button click event"""
    # Get the updated values from the input components
    updated_sub_category = self.text_box_1.text.lower()
    updated_points = int(self.text_box_2.text)

    # Update the existing row in the product_categories table
    if self.selected_row is not None:
      self.selected_row['sub_category'] = updated_sub_category
      self.selected_row['min_points'] = updated_points

      # Save changes to the database
      self.selected_row.update()

      existing_min_points = [row["min_points"] for row in app_tables.fin_admin_ascend_categories.search(group_name="other_loan")]
      max_points = max(existing_min_points + [updated_points])

      existing_group_row  = app_tables.fin_admin_ascend_groups.get(group_name="other_loan")
      if existing_group_row:
        existing_group_row['max_points'] = max_points
        existing_group_row.update()
      else:
        new_group_row = app_tables.fin_admin_ascend_groups.add_row(
          group_name="other_loan", max_points=max_points)

      alert("Changes saved successfully!")
      open_form('admin.dashboard.manage_ascend_score.add_subcategory')

  def delete_click(self, **event_args):
    """This method is called when the Delete button is clicked"""
    # Check if the user confirms the deletion
    if confirm("Are you sure you want to delete this item?"):
      # Delete the row directly on the client side
      self.selected_row.delete()

      existing_min_points = [row["min_points"] for row in app_tables.categories.search(group_name="other_loan")]
      max_points = max(existing_min_points)

      existing_group_row  = app_tables.fin_admin_ascend_groups.get(group_name="other_loan")
      if existing_group_row:
        existing_group_row['max_points'] = max_points
        existing_group_row.update()
      else:
        new_group_row = app_tables.fin_admin_ascend_groups.add_row(
          group_name="other_loan", max_points=max_points)

      # Optionally, navigate to a different form or perform other actions
      open_form('admin.dashboard.manage_ascend_score.add_subcategory')

  def home_button(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard')

  def button_1_copy_3_click(self, **event_args):
    """Cancel button click event"""
    open_form('admin.dashboard.manage_ascend_score.add_subcategory')
