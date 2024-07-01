from ._anvil_designer import All_loansTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class All_loans(All_loansTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    loan_details = app_tables.fin_loan_details.search()
        
        # Prepare data for displaying in UI
    combined_data = []
    for loan in loan_details:
            combined_data.append({
                'lender_email_id': loan['lender_email_id'],
                'lender_full_name': loan['lender_full_name'],
                'lender_customer_id': loan['lender_customer_id'],
                'membership_type': loan['membership_type'],
                'product_name': loan['product_name'],
                'loan_amount': loan['loan_amount'],
                'loan_updated_status': loan['loan_updated_status'],
                'borrower_full_name': loan['borrower_full_name'],
                'borrower_customer_id': loan['borrower_customer_id'],
                'borrower_email_id': loan['borrower_email_id']
            })
        
        # Bind data to the DataGrid component
    self.repeating_panel_1.items = combined_data
     

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.loan_management.application_intake')

