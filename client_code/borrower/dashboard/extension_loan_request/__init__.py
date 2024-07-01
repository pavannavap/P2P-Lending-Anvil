from ._anvil_designer import extension_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class extension_loan_request(extension_loan_requestTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId
        print("user", self.user_id)
        

        # Fetch theuser profile record based on the current user's email
        user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
        # Check if the user profile record is found
        if user_profile:
            # Access the user ID from the user profile record
            user_id = user_profile['customer_id']
            # Filter loan_details table based on the current user's ID
            try:
                customer_loans = app_tables.fin_loan_details.search(loan_updated_status=q.any_of("disbursed", "extension"), borrower_customer_id=user_id)
                loans = []
                for loan in customer_loans:
                    lender_details = app_tables.fin_user_profile.get(customer_id=loan['lender_customer_id'])
                    product_details = app_tables.fin_product_details.get(product_id=loan['product_id'])
                    if user_profile is not None and product_details['extension_allowed'] == 'Yes':
                        loan_data = {
                            'mobile': lender_details['mobile'],
                            'interest_rate': loan['interest_rate'],
                            'loan_amount': loan['loan_amount'],
                            'tenure': loan['tenure'],
                            'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                            'product_name': loan['product_name'],
                            'product_description': loan['product_description'],
                            'lender_full_name': loan['lender_full_name'],
                            'product_id': loan['product_id'],
                            'loan_id': loan['loan_id'],
                            'borrower_full_name': loan['borrower_full_name'],
                            'loan_updated_status': loan['loan_updated_status'],
                            'emi_payment_type': loan['emi_payment_type'],
                            'eligible': self.is_loan_eligible(loan),
                            'user_photo': lender_details['user_photo'],
                            'lender_returns' : loan['lender_returns'],
                              'remaining_amount' : loan['remaining_amount'],
                              'total_repayment_amount' : loan['total_repayment_amount'],
                              'total_interest_amount' : loan['total_interest_amount'],
                        }
                        loans.append(loan_data)

                # Set the filtered data as the items for the repeating panel
                self.repeating_panel_2.items = loans
            except anvil.tables.TableError as e:
                print(f"Error: {e}")
        else:
            # Handle the case when no user profile record is found
            print("User profile record not found for the current user.")

    def is_loan_eligible(self, loan):
        # Check eligibility based on 'extension_allowed' from product_details
        product_details_record = app_tables.fin_product_details.get(product_id=loan['product_id'])
        return product_details_record['extension_allowed'] == 'Yes'


