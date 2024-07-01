from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from ...bank_users.user_form import user_module

class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email = main_form_module.email
    self.user_id = main_form_module.userId
    print(self.user_id, "user_ID")
    self.email = self.email
    self.user_id = self.user_id
    self.load_data(None)
    self.update_platform_fees()


    user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_profile:
      self.image_5.source = user_profile['user_photo']
      self.label_11.text = "Welcome " + user_profile['full_name']
      
    existing_loans = app_tables.fin_loan_details.search(loan_updated_status=q.any_of(
                          q.like('under process%'),
                          q.like('Under Process%'),
                          q.like('under process')))
    self.label_9.text = str(len(existing_loans) or 0)

    investment = app_tables.fin_lender.get(customer_id=self.user_id)
    self.label_3.text = investment['present_commitments'] or 0
    self.label_13.text = str(investment['membership'])
    self.label_15.text = str(investment['member_since'])

    opening_bal = app_tables.fin_wallet.get(customer_id=self.user_id)   
    self.label_2_copy.text = "{:.2f}".format((opening_bal['wallet_amount'] or 0))
    self.label_4_copy.text =  "{:.2f}".format((opening_bal['wallet_amount'] or 0))

    my_returns = app_tables.fin_lender.get(customer_id=self.user_id)
    self.label_7.text = str(my_returns['return_on_investment'] or 0)

    disbursed_loan = app_tables.fin_loan_details.search(loan_updated_status=q.like('disbursed%'), lender_customer_id=self.user_id)
    lost_opportunities = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'), lender_customer_id=self.user_id)
    closed = app_tables.fin_loan_details.search(loan_updated_status=q.like('closed%'), lender_customer_id=self.user_id)
    extended = app_tables.fin_loan_details.search(loan_updated_status=q.like('extension%'), lender_customer_id=self.user_id)
    
    self.button_1_copy.text = f"New Loan Requests ({len(existing_loans)})"
    self.button_2_copy.text = f"Loan Disbursed ({len(disbursed_loan)})"
    self.button_3_copy.text = f"Lost Opportunities ({len(lost_opportunities)})"
    self.button_4_copy.text = f"Closed ({len(closed)})"
    self.button_5_copy.text = f"Extended ({len(extended)})"
    # self.column_panel_8.width = '100%'

    # Any code you write here will run before the form opens.

  
  def update_platform_fees(self, **event_args):
      # Call the server function to update the fees
      result = anvil.server.call('update_fin_platform_fees')
      if result is not None:
          alert(result)
  
  def load_data(self, status):
    if status == 'closed':
      closed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('closed%'), lender_customer_id=self.user_id)
      self.new_loan = len(closed_loans)
      self.repeating_panel_1.items = self.process_data(closed_loans)
    elif status == 'disbursed':
      disbursed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('disbursed%'), lender_customer_id=self.user_id)
      self.repeating_panel_1.items = self.process_data(disbursed_loans)
    elif status == 'under process':
      underprocess_loans = app_tables.fin_loan_details.search(loan_updated_status=q.any_of(q.like('under process%'), q.like('under process')))
      self.repeating_panel_2.items = self.process_data(underprocess_loans)
    elif status == 'lost opportunities':
      lost_opportunities = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'), lender_customer_id=self.user_id)
      self.repeating_panel_1.items = self.process_data(lost_opportunities)
    elif status == 'extension':
      extension_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('extension%'), lender_customer_id=self.user_id)
      self.repeating_panel_1.items = self.process_data(extension_loans)

  def process_data(self, data):
    profiles_with_loans = []
    for loan in data:
      user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
      if user_profile is not None:
        profiles_with_loans.append({
          'loan_amount': loan['loan_amount'],
          'tenure': loan['tenure'],
          'borrower_full_name': loan['borrower_full_name'],
          'loan_id': loan['loan_id'],
          'ascend_value': user_profile['ascend_value'],
          'loan_updated_status': loan['loan_updated_status'],
          'interest_rate': loan['interest_rate'],
          'borrower_loan_created_timestamp': loan['borrower_loan_created_timestamp'],
          'borrower_customer_id': loan['borrower_customer_id'],
          'ascend_score': user_profile['ascend_value'],
          'credit_limit': loan['credit_limit'],
          'product_name': loan['product_name']
        })
    return profiles_with_loans

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.dasboard_contact")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard.dasboard_about')

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard.dashboard_report_a_problem')

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.lender_view_profile")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_borrower_loan_request")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_loan_extension_requests")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_loan_foreclosure_Requests")

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.today_dues")

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.lender_view_loans")

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_lost_oppurtunities")

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.change_password")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_transaction_history")

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    customer_id = self.user_id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_or_send_notifications")

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.data_grid_new_loan_request.visible = False
    self.repeating_panel_1.visible = False
    self.data_grid_1.visible = True
    self.repeating_panel_2.visible = True
    self.load_data('under process')

  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.data_grid_1.visible = False
    self.repeating_panel_2.visible = False
    self.data_grid_new_loan_request.visible = True
    self.repeating_panel_1.visible = True
    self.load_data('disbursed loan')

  def button_3_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.data_grid_1.visible = False
    self.repeating_panel_2.visible = False
    self.data_grid_new_loan_request.visible = True
    self.repeating_panel_1.visible = True
    self.load_data('lost opportunities')

  def button_4_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.data_grid_1.visible = False
    self.repeating_panel_2.visible = False
    self.data_grid_new_loan_request.visible = True
    self.repeating_panel_1.visible = True
    self.load_data('close')

  def button_5_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.data_grid_1.visible = False
    self.repeating_panel_2.visible = False
    self.data_grid_new_loan_request.visible = True
    self.repeating_panel_1.visible = True
    self.load_data('extension')

  def label_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard.my_returns')

  def label_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard.lender_commitments_chart')

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    customer_id = self.user_id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def link_14_click(self, **event_args):
    """This method is called when the link is clicked"""
    customer_id = self.user_id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    customer_id = self.user_id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def link_15_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.lender_view_profile")

  def link_16_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.borrower_portfolio_first_page')


