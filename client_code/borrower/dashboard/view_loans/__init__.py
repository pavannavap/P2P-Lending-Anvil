from ._anvil_designer import view_loansTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class view_loans(view_loansTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId
        self.load_data()

    def load_data(self):
          # Retrieve and display open loans
          open_loans = app_tables.fin_loan_details.search(
              loan_updated_status=q.any_of(
                  q.like('disbursed%'),
                  q.like('foreclosure%'),
                  q.like('extension%')
              ),
            borrower_customer_id=self.user_id
          )
          self.repeating_panel_6.items = self.process_data(open_loans)
          self.label_5.text = str(len(self.repeating_panel_6.items))
  
          # Retrieve and display closed loans
          closed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('closed%'), borrower_customer_id=self.user_id)
          self.repeating_panel_7.items = self.process_data(closed_loans)
          self.label_6.text = str(len(self.repeating_panel_7.items))
  
          # Retrieve and display rejected loans
          rejected_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('rejected%'), borrower_customer_id=self.user_id)
          self.repeating_panel_8.items = self.process_data(rejected_loans)
          self.label_7.text = str(len(self.repeating_panel_8.items))
  
          # Retrieve and display underprocess loans
          underprocess_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('under process%'), borrower_customer_id=self.user_id)
          self.repeating_panel_9.items = self.process_data(underprocess_loans)
          self.label_8.text = str(len(self.repeating_panel_9.items))
  
          # Retrieve and display foreclosure loans
          foreclosure_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('foreclosure%'), borrower_customer_id=self.user_id)
          self.repeating_panel_10.items = self.process_data(foreclosure_loans)
          self.label_9.text = str(len(self.repeating_panel_10.items))
  
    def process_data(self, data):
      profiles_with_loans = []
      for loan in data:
          # user_profile = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
          # user_profile_1 = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
          # if user_profile is not None and user_profile_1 is not None:
              profiles_with_loans.append({
                  # 'mobile': user_profile['mobile'],
                  'interest_rate': loan['interest_rate'],
                  'loan_amount': loan['loan_amount'],
                  'tenure': loan['tenure'],
                  'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                  'product_name': loan['product_name'],
                  'product_description': loan['product_description'],
                  'borrower_full_name': loan['borrower_full_name'],
                  'loan_id': loan['loan_id'],
                  'borrower_loan_created_timestamp': loan['borrower_loan_created_timestamp'],
                  'loan_updated_status': loan['loan_updated_status'],
                  'lender_full_name': loan['lender_full_name'],
                  # 'mobile_1' : user_profile_1['mobile']
              })
      return profiles_with_loans
    

        

        # self.repeating_panel_7.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'), borrower_customer_id=self.user_id)
        # self.repeating_panel_8.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('reject%'), borrower_customer_id=self.user_id)
        # self.repeating_panel_9.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('under process%'), borrower_customer_id=self.user_id)
        # self.repeating_panel_10.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('foreclosure%'), borrower_customer_id=self.user_id)

        # Update label texts with the count of items in each repeating panel
      # self.label_5.text = str(len(self.repeating_panel_6.items))
      # self.label_6.text = str(len(self.repeating_panel_7.items))
      # self.label_7.text = str(len(self.repeating_panel_8.items))
      # self.label_8.text = str(len(self.repeating_panel_9.items))
      # self.label_9.text = str(len(self.repeating_panel_10.items))

    def home_borrower_registration_form_copy_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = True
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = False
        self.repeating_panel_6.visible = True
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = True
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = True
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False 

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = True
        self.label_4.visible = False
        self.label_10.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = True
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = True
        self.label_10.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = True
        self.repeating_panel_10.visible = False

    def button_5_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = True
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = True  

