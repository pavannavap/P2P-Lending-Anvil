# from ._anvil_designer import lender_revenue_shareTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class lender_revenue_share(lender_revenue_shareTemplate):
#   def __init__(self, customer_id, **properties):
#     # Call the initializer of the parent class
#     self.init_components(**properties)
#     self.customer_id = customer_id
#     self.load_loan_data()

#   def load_loan_data(self):

#     loans = app_tables.fin_loan_details.search(loan_updated_status= q.any_of(q.like('closed loan'),q.like('foreclosure'),q.like('extension'),q.like('disbursed loan')),lender_customer_id=self.customer_id)
#     loan_details = []

#     for loan in loans:
#       product_id = loan['product_id']
#       tds_percentage = self.get_tds_percentage(product_id)
#       lender_returns = loan['lender_returns'] or 0  # Ensure lender_returns is not None
#       tds_on_lender_roi = self.calculate_tds_on_roi(lender_returns, tds_percentage)
#       lender_commission = lender_returns - tds_on_lender_roi  # Calculate Lender Commission

#       loan_details.append({
#         'loan_id': loan['loan_id'],
#         'loan_amount': loan['loan_amount'],
#         'lender_returns': lender_returns,
#         'tds_on_lender_roi': tds_on_lender_roi,
#         'lender_commission': lender_commission
#         # Add other fields as necessary
#       })
    
#     self.repeating_panel_1.items = loan_details
  
#   def get_tds_percentage(self, product_id):
#     # Fetch the TDS percentage from the fin_product_details table based on product_id
#     product_details = app_tables.fin_product_details.get(product_id=product_id)
#     if product_details:
#       return product_details['tds'] or 0  # Ensure tds is not None
#     return 0
  
#   def calculate_tds_on_roi(self, lender_roi, tds_percentage):
#     return (lender_roi * tds_percentage) / 100  # Calculate TDS on Lender ROI

#   def button_1_click(self, **event_args):
#     open_form("admin.dashboard.revenue_share")







from ._anvil_designer import lender_revenue_shareTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_revenue_share(lender_revenue_shareTemplate):
  def __init__(self, customer_id, **properties):
    # Call the initializer of the parent class
    self.init_components(**properties)
    self.customer_id = customer_id
    self.load_loan_data()

  def load_loan_data(self):
    loans = app_tables.fin_loan_details.search(loan_updated_status= q.any_of(q.like('closed'),q.like('foreclosure'),q.like('extension'),q.like('disbursed')),lender_customer_id=self.customer_id)

    # Fetch loans based on desired statuses and customer_id
    # loans = app_tables.fin_loan_details.search(
    #   q.all_of(
    #     q.any_of(
    #       q.like('loan_updated_status', 'closed loan'),
    #       q.like('loan_updated_status', 'foreclosure'),
    #       q.like('loan_updated_status', 'extension'),
    #       q.like('loan_updated_status', 'disbursed loan')
    #     ),
    #     q.ilike('lender_customer_id', self.customer_id)
    #   )
    # )

    loan_details = []

    for loan in loans:
      product_id = loan['product_id']
      tds_percentage = self.get_tds_percentage(product_id)
      lender_returns = loan['lender_returns'] or 0  # Ensure lender_returns is not None
      tds_on_lender_roi = self.calculate_tds_on_roi(lender_returns, tds_percentage)
      lender_commission = lender_returns - tds_on_lender_roi  # Calculate Lender Commission
      extra_fee_total = self.calculate_total_extra_fee(loan['loan_id'])  # Calculate total extra fee

      loan_details.append({
        'loan_id': loan['loan_id'],
        'loan_amount': loan['loan_amount'],
        'lender_returns': lender_returns,
        'tds_on_lender_roi': tds_on_lender_roi,
        'lender_commission': lender_commission,
        'extra_fee_total': extra_fee_total  # Add total extra fee to the loan details
      })
    
    self.repeating_panel_1.items = loan_details

  def get_tds_percentage(self, product_id):
    # Fetch the TDS percentage from the fin_product_details table based on product_id
    product_details = app_tables.fin_product_details.get(product_id=product_id)
    if product_details:
      return product_details['tds'] or 0  # Ensure tds is not None
    return 0

  def calculate_tds_on_roi(self, lender_roi, tds_percentage):
    return (lender_roi * tds_percentage) / 100  # Calculate TDS on Lender ROI

  def calculate_total_extra_fee(self, loan_id):
    # Fetch all records from fin_emi table based on loan_id and sum the extra_fee
    emis = app_tables.fin_emi_table.search(loan_id=loan_id)
    total_extra_fee = sum(emi['total_platform_fee'] or 0 for emi in emis)  # Ensure extra_fee is not None
    return total_extra_fee

  def button_1_click(self, **event_args):
    open_form("admin.dashboard.accounting.revenue_share")
