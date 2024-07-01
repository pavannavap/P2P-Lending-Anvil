from ._anvil_designer import view_profile_8Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_profile_8(view_profile_8Template):
    def __init__(self, loan_id_to_display, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
    
        self.loan_data = app_tables.fin_loan_details.get(loan_id=loan_id_to_display)
        if self.loan_data:
            user_profile_data = app_tables.fin_user_profile.get(customer_id=self.loan_data['borrower_customer_id'])
            if user_profile_data:
              self.label_34.text = user_profile_data['usertype']

            # Fetch additional data from fin_borrower table based on borrower_customer_id
            borrower_data = app_tables.fin_borrower.get(customer_id=self.loan_data['borrower_customer_id'])
            if borrower_data:
                self.label_26.text = borrower_data['ascend_score']
              
            self.label_2.text = self.loan_data['loan_id']
            self.label_4.text = self.loan_data['borrower_customer_id']
            self.label_6.text = self.loan_data['borrower_full_name']
            # self.label_8.text = self.loan_data['loan_status']
            # self.label_10.text = self.loan_data['application_status']
            # self.label_12.text = self.loan_data['min_amount']
            # self.label_14.text = self.loan_data['max_amount']
            self.label_16.text = self.loan_data['interest_rate']
            self.label_18.text = self.loan_data['borrower_loan_created_timestamp']
            self.label_20.text = self.loan_data['total_repayment_amount']
            # self.label_22.text = self.loan_data['total_payments_made']
            # self.label_24.text = self.loan_data['member_rom']
            self.label_28.text = self.loan_data['borrower_email_id']
            self.label_30.text = self.loan_data['tenure']
            self.label_32.text = self.loan_data['loan_updated_status']



    def back_click(self, **event_args):
      open_form('admin.dashboard.loan_management.view_loans.lapsed_loans')
    
