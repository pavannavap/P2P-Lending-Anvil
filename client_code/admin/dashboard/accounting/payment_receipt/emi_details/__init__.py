from ._anvil_designer import emi_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

class emi_details(emi_detailsTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_row = selected_row
        # Store the selected loan_id
        self.selected_loan_id = selected_row['loan_id']
        
        # Fetch and display data for the selected loan_id
        self.fetch_and_display_data()
        self.button_1.text = "Each EMI"
    
    def fetch_and_display_data(self):
        # Fetch all EMI records for the selected loan_id from the database
        emi_records = app_tables.fin_emi_table.search(loan_id=self.selected_loan_id)
        
        filtered_emis = []
        filtered_emis1 = []

        # Initialize total amount paid
        total_amount_paid = 0.0
        
        # Iterate through each EMI record
        for emi in emi_records:
            # Fetch borrower profile based on EMI's customer_id
            borrower_profile = app_tables.fin_user_profile.get(customer_id=emi['borrower_customer_id'])
            
            # Fetch loan details associated with this EMI
            loan_details = app_tables.fin_loan_details.get(loan_id=emi['loan_id'])
            
            if loan_details:
                # Fetch lender profile based on loan's lender_customer_id
                lender_profile = app_tables.fin_user_profile.get(customer_id=loan_details['lender_customer_id'])
            else:
                lender_profile = None

            self.label_6.text = borrower_profile['full_name'] if borrower_profile else None
            self.label_7.text = borrower_profile['mobile'] if borrower_profile else None
            self.label_8.text = borrower_profile['street_adress_1'] if borrower_profile else None
            self.label_9.text = lender_profile['full_name'] if lender_profile else None
            self.label_10.text = lender_profile['mobile'] if lender_profile else None
            self.label_11.text = lender_profile['street_adress_1'] if lender_profile else None

            amount_paid = emi['amount_paid'] if emi['amount_paid'] is not None else 0.0
            total_amount_paid += amount_paid
            self.label_13.text = total_amount_paid
            
            filtered_emis1.append({
                'borrower_name': borrower_profile['full_name'] if borrower_profile else None,
                'lender_name': lender_profile['full_name'] if lender_profile else None,
                'amount_paid': f"{emi['amount_paid']:.2f}" if emi['amount_paid'] is not None else None,
                'loan_id': emi['loan_id'],
                'emi_number': emi['emi_number'],
                'payment_date': emi['scheduled_payment_made'],
                'next_payment_date': emi['next_payment'],
                'total_remaining_amount': f"{emi['total_remaining_amount']:.2f}" if emi['total_remaining_amount'] is not None else None,
                'remaining_tenure': emi['remaining_tenure'],
                'loan_amount': f"{loan_details['loan_amount']:.2f}" if loan_details and loan_details['loan_amount'] is not None else None,
                'total_repayment_amount': f"{loan_details['total_repayment_amount']:.2f}" if loan_details and loan_details['total_repayment_amount'] is not None else None
            })
            self.repeating_panel_2.items = filtered_emis1
            
            # Collect EMI details and borrower/lender information
            filtered_emis.append({
                'borrower_name': borrower_profile['full_name'] if borrower_profile else None,
                'lender_name': lender_profile['full_name'] if lender_profile else None,
                'amount_paid': f"{emi['amount_paid']:.2f}" if emi['amount_paid'] is not None else None,
                'loan_id': emi['loan_id'],
                'emi_number': emi['emi_number'],
                'payment_date': emi['scheduled_payment_made'],
                'next_payment_date': emi['next_payment'],
                'total_remaining_amount': f"{emi['total_remaining_amount']:.2f}" if emi['total_remaining_amount'] is not None else None,
                'remaining_tenure': emi['remaining_tenure'],
                'loan_amount': f"{loan_details['loan_amount']:.2f}" if loan_details and loan_details['loan_amount'] is not None else None,
                'total_repayment_amount': f"{loan_details['total_repayment_amount']:.2f}" if loan_details and loan_details['total_repayment_amount'] is not None else None
            })
        
        # Display the filtered EMIs in a repeating panel or similar component
        self.repeating_panel_1.items = filtered_emis

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.button_1.text == "Each EMI":
            self.button_1.text = "Overall EMI's"
            self.data_grid_1.visible = True
            self.content.visible = False
            self.label_1.visible = True
        else:
            self.button_1.text = "Each EMI"
            self.data_grid_1.visible = False
            self.content.visible = True
            self.label_1.visible = False

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.accounting.payment_receipt')

    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      # pdf = anvil.server.call('create_receipt_pdf1')
      # anvil.media.download(pdf)
      self.convert_panel_to_pdf()

    def convert_panel_to_pdf(self):
      # Assuming 'content_panel' is the panel containing your data
      content_panel = self.content
      
      # Call the server function to create the PDF from the content panel
      pdf = anvil.server.call('create_pdf_from_panel', content_panel)
      
      # Prompt the user to download the PDF
      anvil.media.download(pdf)