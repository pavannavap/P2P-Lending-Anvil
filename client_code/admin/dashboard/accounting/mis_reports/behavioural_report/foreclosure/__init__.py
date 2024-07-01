from ._anvil_designer import foreclosureTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class foreclosure(foreclosureTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.load_foreclosure_data()

    def load_foreclosure_data(self):
        # Fetch data from the fin_loan_details table where loan_updated_status is 'foreclosure'
        loan_details = app_tables.fin_loan_details.search(loan_updated_status="foreclosure")
        
        borrower_loans = {}
        
        # Process the data to aggregate loans by borrower
        for loan in loan_details:
            borrower_id = loan['borrower_customer_id']
            if borrower_id not in borrower_loans:
                user_profile = app_tables.fin_user_profile.get(customer_id=borrower_id)
                mobile_no = user_profile['mobile'] if user_profile else None
                
                borrower_loans[borrower_id] = {
                    'borrower_full_name': loan['borrower_full_name'],
                    'borrower_email_id': loan['borrower_email_id'],
                    'mobile_no': mobile_no,
                    'loans': [],
                    'product_names': set()  # Initialize a set for product names
                }
            borrower_loans[borrower_id]['loans'].append(loan)
            borrower_loans[borrower_id]['product_names'].add(loan['product_name'])  # Add product name to the set
        
        # Filter borrowers with two or more foreclosure loans
        result = []
        for borrower_id, details in borrower_loans.items():
            if len(details['loans']) >= 2:
                result.append({
                    'borrower_customer_id': borrower_id,
                    'borrower_full_name': details['borrower_full_name'],
                    'borrower_email_id': details['borrower_email_id'],
                    'mobile_no': details['mobile_no'],
                    'loans_count': len(details['loans']),
                    'product_names': ", ".join(details['product_names'])  # Convert set to a comma-separated string
                })
        
        # Set the filtered data to the repeating panel
        self.repeating_panel_1.items = result

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.accounting.mis_reports.behavioural_report')
