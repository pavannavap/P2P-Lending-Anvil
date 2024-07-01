# from ._anvil_designer import RowTemplate32Template
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables


# class RowTemplate32(RowTemplate32Template):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     print("id", self.item['customer_id'])

#     # Assuming self.item contains the row data
#     disbursed_list = list(app_tables.fin_loan_details.search(lender_customer_id=self.item['customer_id']))
#     disbursed = disbursed_list[0] if disbursed_list else None
    
#     if disbursed:
#         self.status = disbursed['loan_updated_status']
#         print(f"Status for customer {self.item['customer_id']}: {self.status}")
#     else:
#         self.status = None
#         print(f"No disbursed record found for customer {self.item['customer_id']}")
    
#     # Set visibility based on the status
#     if self.status == "disbursed":
#         self.portfolio.visible = True
#         print(f"Link visible for customer {self.item['customer_id']}: {self.portfolio.visible}")
#     else:
#         self.portfolio.visible = False
#         print(f"Link not visible for customer {self.item['customer_id']}: {self.portfolio.visible}")
    
#   def portfolio_click(self, **event_args):
#       """This method is called when the link is clicked"""
#       selected_row = self.item
#       open_form('lendor.dashboard.lender_portfolio', selected_row=selected_row)
    

from ._anvil_designer import RowTemplate32Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate32(RowTemplate32Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        print("id", self.item['customer_id'])

        # Assuming self.item contains the row data
        disbursed_list = list(app_tables.fin_loan_details.search(lender_customer_id=self.item['customer_id']))
        
        # Check if any of the disbursed_list has 'loan_updated_status' as 'disbursed'
        self.status = None
        for record in disbursed_list:
            if record['loan_updated_status'] == 'disbursed':
                self.status = 'disbursed'
                break
        
        print(f"Status for customer {self.item['customer_id']}: {self.status}")

        # Set visibility based on the status
        if self.status == "disbursed":
            self.portfolio.visible = True
            print(f"Link visible for customer {self.item['customer_id']}: {self.portfolio.visible}")
        else:
            self.portfolio.visible = False
            print(f"Link not visible for customer {self.item['customer_id']}: {self.portfolio.visible}")

    def portfolio_click(self, **event_args):
        """This method is called when the link is clicked"""
        selected_row = self.item
        open_form('lendor.dashboard.lender_portfolio', selected_row=selected_row)
