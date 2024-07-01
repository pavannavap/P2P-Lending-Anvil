from ._anvil_designer import lender_portfolio_first_pageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....bank_users.main_form import main_form_module
from ....bank_users.user_form import user_form
from ....bank_users.user_form import user_module


class lender_portfolio_first_page(lender_portfolio_first_pageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        self.email = main_form_module.email
        self.user_Id = main_form_module.userId

        self.data = tables.app_tables.fin_lender.search()

        if not self.data:
            Notification("No Data Available Here!").show()
        else:
            self.result = [{'name': i['user_name'],
                            'email': i['email_id'],
                            'lending_type': i['lending_type'],
                            'membership': i['membership'],
                            'customer_id': i['customer_id']
                           }
                          for i in self.data]

            self.repeating_panel_1.items = self.result

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor.dashboard')

        
