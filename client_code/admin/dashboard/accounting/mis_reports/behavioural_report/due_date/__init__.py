from ._anvil_designer import due_dateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class due_date(due_dateTemplate):
    def __init__(self, **properties):
    # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.due_date_data()

    def due_date_data(self):
        emi_details = app_tables.fin_emi_table.search(days_left=q.greater_than_or_equal_to(2))
        
        loan_emi_count = {}
        
        # Count the number of EMIs for each loan
        for emi in emi_details:
            loan_id = emi['loan_id']
            if loan_id not in loan_emi_count:
                loan_emi_count[loan_id] = 0
            loan_emi_count[loan_id] += 1
        
        unique_loans = set()  # A set to keep track of already added loan IDs
        result = []
        for emi in emi_details:
            loan_id = emi['loan_id']
            if loan_emi_count[loan_id] >= 2 and loan_id not in unique_loans:  # Check if the number of EMIs for this loan is >= 2 and not already added
                borrower_id = emi['borrower_customer_id']
                user_profile = app_tables.fin_user_profile.get(customer_id=borrower_id)
                mobile_no = user_profile['mobile'] if user_profile else None

                result.append({
                    'loan_id': loan_id,
                    'borrower_customer_id': borrower_id,
                    'borrower_full_name': user_profile['full_name'] if user_profile else None,
                    'borrower_email_id': user_profile['email_user'] if user_profile else None,
                    'mobile_no': mobile_no,
                    'days_left': 'Late Payment'
                    # 'days_left': emi['days_left']
                })
                unique_loans.add(loan_id)  # Mark this loan ID as added
        
        # Debug: Print the final result before setting it to the repeating panel
        print("Final result:", result)
        
        # Set the filtered data to the repeating panel
        self.repeating_panel_1.items = result

    def button_1_click(self, **event_args):
      open_form('admin.dashboard.accounting.mis_reports.behavioural_report')
