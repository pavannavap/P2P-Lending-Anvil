from ._anvil_designer import application_trackerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class application_tracker(application_trackerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id=main_form_module.userId
    
    
    
    # Any code you write here will run before the form oopens.
    under_process_items = app_tables.fin_loan_details.search(loan_updated_status=q.like('under proces%'), borrower_customer_id=self.user_id)
    borrower_profiles = []
    for loan in under_process_items:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
            if user_profile is not None:
                borrower_profiles.append({
                    'mobile': user_profile['mobile'],
                    'interest_rate': loan['interest_rate'],
                    'loan_amount': loan['loan_amount'],
                    'tenure': loan['tenure'],
                    'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                    'product_name': loan['product_name'],
                    'product_description': loan['product_description'],
                    'borrower_full_name': loan['borrower_full_name'],
                    'product_id': loan['product_id'],
                    'loan_id': loan['loan_id'],
                    'borrower_loan_created_timestamp':loan['borrower_loan_created_timestamp'],
                    'loan_updated_status' : loan['loan_updated_status']})
                    # 'image_1' : user_profile['user_photo']})
              
    self.repeating_panel_2.items = borrower_profiles
    #self.label_1.text = str(len(under_process_items))

    approved_items = app_tables.fin_loan_details.search(loan_updated_status=q.like('approved%'), borrower_customer_id=self.user_id)
    borrower_prof = []
    for loan in approved_items:
            user_profiles = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
            if user_profiles is not None:
                borrower_prof.append({
                    'mobile': user_profiles['mobile'],
                    'interest_rate': loan['interest_rate'],
                    'loan_amount': loan['loan_amount'],
                    'tenure': loan['tenure'],
                    'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                    'product_name': loan['product_name'],
                    'product_description': loan['product_description'],
                    'lender_full_name': loan['lender_full_name'],
                    'product_id': loan['product_id'],
                    'loan_id': loan['loan_id'],
                    'borrower_loan_created_timestamp':loan['borrower_loan_created_timestamp'],
                    'loan_updated_status' : loan['loan_updated_status']})
    self.repeating_panel_3.items = borrower_prof
      
  
  def home_borrower_registration_button_click(self, **event_args):
    open_form('borrower.dashboard')

  def borrower_dashboard_home_linkhome_borrower_registration_button_copy_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard')

