# from ._anvil_designer import revenue_shareTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class revenue_share(revenue_shareTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)
#     self.load_data()

#   # def load_data(self, status):
#   #   if status == 'close':
#   #     closed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('closed%'))
#   #     self.new_loan = len(closed_loans)
#   #     self.repeating_panel_1.items = self.process_data(closed_loans)
#   def load_data(self):
#     lenders = app_tables.fin_lender.search()
#     customer_details = []

#     for lender in lenders:
#       customer_id = lender['customer_id']
#       # loans = app_tables.fin_loan_details.search(lender_customer_id=customer_id)
#       loans = app_tables.fin_loan_details.search(loan_updated_status= q.any_of(q.like('closed loan'),q.like('foreclosure'),q.like('extension'),q.like('disbursed loan')),lender_customer_id=customer_id)
#       loan_count = len(loans)
      
#       user_profile = app_tables.fin_user_profile.get(customer_id=customer_id)
#       mobile_no = user_profile['mobile'] if user_profile else None
#       email = user_profile['email_user'] if user_profile else None
      
#       customer_details.append({
#         'customer_id': customer_id,
#         'name': lender['user_name'],
#         'email': email,
#         'return_on_investment': lender['return_on_investment'],
#         'loan_count': loan_count,
#         'mobile_no': mobile_no,
#       })
    
#     self.repeating_panel_1.items = customer_details

#   def link_1_click(self, **event_args):
#     open_form('admin.dashboard')

#   def button_1_copy_3_click(self, **event_args):
#     open_form('admin.dashboard.manage_settings')

#   def button_1_click(self, **event_args):
#     open_form('admin.dashboard')





from ._anvil_designer import revenue_shareTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class revenue_share(revenue_shareTemplate):
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

  def link_1_click(self, **event_args):
    open_form('admin.dashboard')

  def button_1_copy_3_click(self, **event_args):
    open_form('admin.dashboard.manage_settings')

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.accounting')
