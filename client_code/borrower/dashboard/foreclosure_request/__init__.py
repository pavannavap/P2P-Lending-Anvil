# from ._anvil_designer import foreclosure_requestTemplate
# from anvil import *
# import anvil.server
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# from .. import main_form_module as main_form_module

# class foreclosure_request(foreclosure_requestTemplate):
#     def __init__(self, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)
#         self.user_id = main_form_module.userId
#         print("user", self.user_id)

#         # Fetch the user profile record based on the current user's ID
#         user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
#         # Check if the user profile record is found
#         if user_profile:
#             # Filter loan_details table based on the current user's ID and loan status
#             try:
#                 customer_loans = [loan for loan in app_tables.fin_loan_details.search(borrower_customer_id=self.user_id) if loan['loan_updated_status'] in ['disbursed loan', 'foreclosure']]
#                 loans = []
#                 for loan in customer_loans:
#                     if user_profile is not None:
#                         lender_photo = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
#                         # Check if the loan product is eligible for foreclosure
#                         product_details_record = app_tables.fin_product_details.get(product_id=loan['product_id'])
#                         if product_details_record['foreclose_type'] == 'Eligible':
#                             loan_data = {
#                                 'mobile': lender_photo['mobile'],
#                                 'interest_rate': loan['interest_rate'],
#                                 'loan_amount': loan['loan_amount'],
#                                 'tenure': loan['tenure'],
#                                 'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
#                                 'product_name': loan['product_name'],
#                                 'product_description': loan['product_description'],
#                                 'lender_full_name': loan['lender_full_name'],
#                                 'product_id': loan['product_id'],
#                                 'loan_id': loan['loan_id'],
#                                 'loan_updated_status': loan['loan_updated_status'],
#                                 'emi_payment_type': loan['emi_payment_type'],
#                                 'credit_limit' : loan['credit_limit'],
#                                 'foreclosure_type' : loan['foreclosure_type'],
#                                 'borrower_full_name' : loan['borrower_full_name'],
#                                 'user_photo':lender_photo['user_photo']
#                             }
#                             loans.append(loan_data)

#                 # Set the filtered data as the items for the repeating panel
#                 self.repeat.items = loans
#             except anvil.tables.TableError as e:
#                 print(f"Error: {e}")
#         else:
#             # Handle the case when no user profile record is found
#             print("User profile record not found for the current user.")

#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form('borrower_registration_form.dashboard')



from ._anvil_designer import foreclosure_requestTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class foreclosure_request(foreclosure_requestTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId
        print("user", self.user_id)

        # Fetch the user profile record based on the current user's ID
        user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
        # Check if the user profile record is found
        if user_profile:
            # Filter loan_details table based on the current user's ID and loan status
            try:
                customer_loans = [loan for loan in app_tables.fin_loan_details.search(borrower_customer_id=self.user_id) if loan['loan_updated_status'] in ['disbursed', 'foreclosure']]
                loans = []
                for loan in customer_loans:
                    if user_profile is not None:
                        lender_photo = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
                        # Check if the loan product is eligible for foreclosure
                        product_details_record = app_tables.fin_product_details.get(product_id=loan['product_id'])
                        if product_details_record['foreclose_type'] == 'Eligible':
                            # Check if there are any records in fin_emi_table associated with this loan
                            emi_rows = app_tables.fin_emi_table.search(loan_id=loan['loan_id'])
                            if emi_rows:
                                loan_data = {
                                    'mobile': lender_photo['mobile'],
                                    'interest_rate': loan['interest_rate'],
                                    'loan_amount': loan['loan_amount'],
                                    'tenure': loan['tenure'],
                                    'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                                    'product_name': loan['product_name'],
                                    'product_description': loan['product_description'],
                                    'lender_full_name': loan['lender_full_name'],
                                    'product_id': loan['product_id'],
                                    'loan_id': loan['loan_id'],
                                    'loan_updated_status': loan['loan_updated_status'],
                                    'emi_payment_type': loan['emi_payment_type'],
                                    'credit_limit' : loan['credit_limit'],
                                    'foreclosure_type' : loan['foreclosure_type'],
                                    'borrower_full_name' : loan['borrower_full_name'],
                                    'user_photo': lender_photo['user_photo'],
                                    'lender_customer_id' : loan['lender_customer_id'],
                                    'borrower_customer_id' : loan['borrower_customer_id'],
                                    'lender_email_id' : loan['lender_email_id'],
                                    'borrower_email_id' : loan['borrower_email_id'],
                                    'lender_returns' : loan['lender_returns'],
                                    'remaining_amount' : loan['remaining_amount'],
                                    'total_repayment_amount' : loan['total_repayment_amount'],
                                    'total_interest_amount' : loan['total_interest_amount'],
                                }
                                loans.append(loan_data)

                # Set the filtered data as the items for the repeating panel
                self.repeat.items = loans
            except anvil.tables.TableError as e:
                print(f"Error: {e}")
        else:
            # Handle the case when no user profile record is found
            print("User profile record not found for the current user.")


