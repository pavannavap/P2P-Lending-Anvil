from ._anvil_designer import ItemTemplate69Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class ItemTemplate69(ItemTemplate69Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user_id = main_form_module.userId 
    print(self.user_id)
    user_data = app_tables.fin_loan_details.search(loan_updated_status=q.like('approved%'), borrower_customer_id=self.user_id)
    for row in user_data:
        borrower_customer_id = row['borrower_customer_id']
        lender_customer_id = row['lender_customer_id']
        borrower_profile = app_tables.fin_user_profile.get(customer_id=borrower_customer_id)
        lender_profile = app_tables.fin_user_profile.get(customer_id=lender_customer_id)
        self.image_1.source = lender_profile['user_photo']

  # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row=self.item
    open_form('borrower.dashboard.application_tracker.view_profile',selected_row=selected_row)
