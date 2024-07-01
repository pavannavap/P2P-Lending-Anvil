from ._anvil_designer import payment_receiptTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class payment_receipt(payment_receiptTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.fetch_and_display_data()

    # Any code you write here will run before the form opens.

  def fetch_and_display_data(self):
    # Fetch loan details with loan_updated_status "disbursed" or "extension"
    loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of("disbursed" , "extension" ))
    
    filtered_loans = []
    
    # Iterate through each loan detail
    for loan_detail in loan_details:
        # Collect loan details
        filtered_loans.append({
            'loan_id': loan_detail['loan_id'],
            'borrower_name': loan_detail['borrower_full_name'],
            'lender_name': loan_detail['lender_full_name'],
            'loan_amount': f"{loan_detail['loan_amount']:.2f}",
            'total_repayment_amount': f"{loan_detail['total_repayment_amount']:.2f}",
            'interest_rate': loan_detail['interest_rate'],
            'tenure': loan_detail['tenure']
        })
    
    # Display the filtered loans in a repeating panel or similar component
    self.repeating_panel_1.items = filtered_loans

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting')
