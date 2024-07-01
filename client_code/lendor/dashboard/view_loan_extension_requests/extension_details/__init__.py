from ._anvil_designer import extension_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class extension_details(extension_detailsTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_row = selected_row
        self.name.text = f"{selected_row['borrower_full_name']}"
        self.loan.text = f"{selected_row['loan_amount']}"      
        self.exten_fee.text = f"{selected_row['extend_fee']}"
        self.extension_amount.text = f"{selected_row['extension_amount']}"
        self.total.text = f"{selected_row['total_extension_months']}"
        self.ra.text = f"{selected_row['final_repayment_amount']}"
        self.reason.text = f"{selected_row['reason']}"
        self.new_emi.text = f"{selected_row['new_emi']}"

        if self.selected_row['status'] not in ('approved', 'rejected'):
          approval_days_row = app_tables.fin_approval_days.get(loans='Extension')
        
          if approval_days_row:
              approval_days = approval_days_row['days_for_approval']
              
              # Calculate the time difference between now and the request date
              print("Extension Request Date:", self.selected_row['extension_request_date'])
              time_difference = datetime.now() - datetime.combine(self.selected_row['extension_request_date'], datetime.min.time())
              print("Time Difference (seconds):", time_difference.total_seconds())
  
              # Check if the time difference is more than the approval days
              if time_difference.total_seconds() > (approval_days * 86400):  # 86400 seconds in a day
                  # self.selected_row['status'] = 'approved'
                  # self.selected_row.update()
                  self.update_extension_status('approved')
                  loan = app_tables.fin_loan_details.get(loan_id=self.selected_row['loan_id'])
                  if loan is not None:
                      # Get the current remaining amount
                      current_remaining_amount = loan['remaining_amount'] or 0  # If remaining amount is None, default to 0
                      # Add the extension amount to the current remaining amount
                      new_remaining_amount = current_remaining_amount + self.selected_row['extension_amount']
                      # Update the remaining amount in the loan details table
                      loan['remaining_amount'] = new_remaining_amount
                      loan.update()
                    
                  Notification("Borrower request has been automatically approved.").show()
                  open_form("lendor.dashboard.view_loan_extension_requests")


    def approve_click(self, **event_args):
        """This method is called when the 'Approve' button is clicked"""      
        self.selected_row['status'] = 'approved'
        self.selected_row['status_timestamp '] = datetime.now()
        # Save changes to the table
        self.selected_row.update()
        Notification("Borrower will get notified").show()
    
        self.update_extension_status('approved')

        loan = app_tables.fin_loan_details.get(loan_id=self.selected_row['loan_id'])
        loan['loan_updated_status'] = "extension"
        open_form("lendor.dashboard.view_loan_extension_requests")

    def decline_click(self, **event_args):
        """This method is called when the 'Decline' button zis clicked"""
        self.selected_row['status'] = 'rejected'
        self.selected_row['status_timestamp '] = datetime.now()
        self.selected_row.update()
        self.update_extension_status('rejected')
        Notification("Borrower will get notified").show()
        
        open_form("lendor.dashboard.view_loan_extension_requests")

    def update_extension_status(self, new_status):
        """Update the status in the fin_foreclosure table"""
        foreclosure_row = app_tables.fin_extends_loan.get(loan_id=self.selected_row['loan_id'])
        if foreclosure_row is not None:
            foreclosure_row['status'] = new_status
            foreclosure_row['status_timestamp '] = datetime.now()
            foreclosure_row.update()
            self.approve.visible = False
            self.decline.visible = False
          
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor.dashboard.view_loan_extension_requests')

    def button_1_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor.dashboard')

    def approve_copy_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor.dashboard.view_loan_extension_requests')
