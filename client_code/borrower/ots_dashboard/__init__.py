# from ._anvil_designer import ots_dashboardTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class ots_dashboard(ots_dashboardTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     self.data = tables.app_tables.fin_loan_details.search()

#     a = -1
#     self.list_1 = []
#     self.list_2 = []
#     self.list_3 = []
#     self.list_4 = []
    
    
#     for i in self.data:
#       a+=1
#       self.list_1.append(i['loan_id'])
#       self.list_2.append(i['borrower_customer_id'])
#       self.list_3.append(i['borrower_full_name'])
#       self.list_4.append(i['loan_updated_status'])
#     print(a)

#     self.result = []
#     self.index = []
#     if a == -1:
#       alert("No Data Available Here!")
#     else:
#       b = -1
#       for i in self.list_4:
#         b+=1
#         if i == "OTS" or i == "Approved" or i == 'approved' or i == 'disbursed loan' or i == 'Disbursed loan' or i == 'default loan' or i == 'under process' or i == 'NPA' or i == 'lapsed loan':
#           self.index.append(b)
          
#       for i in self.index:
#         self.result.append({'loan_id' : self.list_1[i], 'coustmer_id' : self.list_2[i], 'full_name' : self.list_3[i], 'loan_status' : self.list_4[i]})

#       self.repeating_panel_1.items = self.result

#       print(self.list_1, self.list_2, self.list_3)
#       print(self.result)
#       print(a)


#     # Any code you write here will run before the form opens.

#   def home_main_form_link_click(self, **event_args):
#     open_form("borrower_registration_form.ots_dashboard")

#   def about_main_form_link_click(self, **event_args):
#     open_form('borrower_registration_form.dashboard.dashboard_about')

#   def contact_main_form_link_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form("borrower_registration_form.dashboard.dashboard_contact")

#   def notification_link_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('lender_registration_form.dashboard.notification')

#   def wallet_dashboard_link_click(self, **event_args):
#         user_profiles = server.call('fetch_user_profiles')
        
#         for profile in user_profiles:
#             result = server.call(
#                 'create_wallet_entry',
#                 profile['email_user'],
#                 profile['customer_id'],
#                 profile['full_name'],
#                 profile['usertype']
#             )
            
#             print(result)
        
#         open_form('wallet.wallet')
        
#         customer_id = 1000
#         email = self.email
#         anvil.server.call('fetch_profile_data_and_insert', email, customer_id)

#   def button_4_click(self, **event_args):
#     open_form('borrower_registration_form.ots_dashboard.my_loans')



from ._anvil_designer import ots_dashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ots_dashboard(ots_dashboardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.data = tables.app_tables.fin_loan_details.search()

        self.result = []
        for loan_detail in self.data:
            if loan_detail['loan_updated_status'] in ['OTS', 'Approved', 'approved', 'disbursed', 'disbursed loan', 'default loan', 'under process', 'NPA', 'lapsed loan']:
                lender_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['lender_customer_id'])
                borrower_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['borrower_customer_id'])
                lender_mobile = lender_profile['mobile'] if lender_profile else None
                borrower_mobile = borrower_profile['mobile'] if borrower_profile else None

                self.result.append({
                    'loan_id': loan_detail['loan_id'],
                    'customer_id': loan_detail['borrower_customer_id'],
                    'full_name': loan_detail['borrower_full_name'],
                    'loan_status': loan_detail['loan_updated_status'],
                     'lender_mobile': lender_mobile,
                    'borrower_mobile': borrower_mobile,
                    'product_name': loan_detail['product_name'],
                    'product_description': loan_detail['product_description'],
                    'tenure': loan_detail['tenure'],
                    'interest_rate': loan_detail['interest_rate'],
                    'loan_disbursed_timestamp': loan_detail['loan_disbursed_timestamp'],
                    'loan_amount': loan_detail['loan_amount'],
                })

        if not self.result:
            alert("No Data Available Here!")
        else:
            self.repeating_panel_2.items = self.result

    def home_main_form_link_click(self, **event_args):
        open_form("borrower.ots_dashboard")

    def about_main_form_link_click(self, **event_args):
        open_form('borrower.dashboard.dashboard_about')

    def contact_main_form_link_click(self, **event_args):
        open_form("borrower.dashboard.dashboard_contact")

    def notification_link_click(self, **event_args):
        open_form('lendor.dashboard.notification')

    def wallet_dashboard_link_click(self, **event_args):
        user_profiles = server.call('fetch_user_profiles')
        
        for profile in user_profiles:
            result = server.call(
                'create_wallet_entry',
                profile['email_user'],
                profile['customer_id'],
                profile['full_name'],
                profile['usertype']
            )
            
            print(result)
        
        open_form('wallet.wallet')
        
        customer_id = 1000
        email = self.email
        anvil.server.call('fetch_profile_data_and_insert', email, customer_id)

    def button_4_click(self, **event_args):
        open_form('borrower.ots_dashboard.my_loans')


