from ._anvil_designer import lender_shareTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class lender_share(lender_shareTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_data()

  def load_data(self):
    lenders = app_tables.fin_lender.search()
    customer_details = []

    for lender in lenders:
      customer_id = lender['customer_id']
      loans = app_tables.fin_loan_details.search(
        loan_updated_status=q.any_of(
          q.like('closed'), q.like('foreclosure'), 
          q.like('extension'), q.like('disbursed')
        ),
        lender_customer_id=customer_id
      )
      loan_count = len(loans)
      
      if loan_count > 0:
        user_profile = app_tables.fin_user_profile.get(customer_id=customer_id)
        mobile_no = user_profile['mobile'] if user_profile else None
        email = user_profile['email_user'] if user_profile else None
        
        customer_details.append({
          'customer_id': customer_id,
          'name': lender['user_name'],
          'email': email,
          'return_on_investment': lender['return_on_investment'],
          'loan_count': loan_count,
          'mobile_no': mobile_no,
        })
    
    self.repeating_panel_1.items = customer_details

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.mis_reports')
