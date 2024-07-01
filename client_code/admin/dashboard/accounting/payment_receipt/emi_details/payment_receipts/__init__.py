from ._anvil_designer import payment_receiptsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class payment_receipts(payment_receiptsTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_row = selected_row
        # Print selected emi_number for debugging
        print(selected_row['emi_number'])
        
        # Store the selected emi_number
        self.emi_number = selected_row['emi_number']
        self.loan_id  = selected_row['loan_id']
        
        # Fetch and display EMI details based on the emi_number
        self.fetch_and_display_data()

    def fetch_and_display_data(self):
        # Fetch EMI record from the database based on the emi_number
        emi_record = app_tables.fin_emi_table.get(emi_number=self.emi_number,loan_id=self.loan_id)
        
        if not emi_record:
            # Handle case where EMI record is not found
            print("EMI record not found")
            return
        
        # Fetch borrower profile based on EMI's customer_id
        borrower_profile = app_tables.fin_user_profile.get(customer_id=emi_record['borrower_customer_id'])
        
        # Fetch loan details associated with this EMI
        loan_details = app_tables.fin_loan_details.get(loan_id=emi_record['loan_id'])
        
        if loan_details:
            # Fetch lender profile based on loan's lender_customer_id
            lender_profile = app_tables.fin_user_profile.get(customer_id=loan_details['lender_customer_id'])
        else:
            lender_profile = None

        self.label_7.text = borrower_profile['full_name'] if borrower_profile else None
        self.label_8.text = borrower_profile['mobile'] if borrower_profile else None
        self.label_19.text = borrower_profile['street_adress_1'] if borrower_profile else None
        self.label_13.text = lender_profile['full_name'] if lender_profile else None
        self.label_14.text = lender_profile['mobile'] if lender_profile else None
        self.label_21.text = lender_profile['street_adress_1'] if lender_profile else None
        # self.label_27.text = emi_record['scheduled_payment_made'] if emi_record else None
        date_only = emi_record['scheduled_payment_made'].date() if emi_record else None

        # Convert to string if needed
        self.label_27.text = date_only.strftime('%Y-%m-%d') if date_only else None
        self.label_29.text = "Online"
        self.label_30.text = emi_record['amount_paid'] if emi_record else None

        

        # Prepare the EMI details for the repeating panel
        filtered_emis = [{
            'borrower_name': borrower_profile['full_name'] if borrower_profile else None,
            'borrower_mobile': borrower_profile['mobile'] if borrower_profile else None,
            'amount_paid': emi_record['amount_paid'],
            'loan_id': emi_record['loan_id'],
            'payment_date': emi_record['scheduled_payment_made'],
            'next_payment_date': emi_record['next_payment'],
            'total_remaining_amount': emi_record['total_remaining_amount'],        
            'payment_type': "Online",
            'loan_amount': loan_details['loan_amount'] if loan_details else None,
            'total_repayment_amount': loan_details['total_repayment_amount'] if loan_details else None
        }]
        
        # Display the filtered EMIs in a repeating panel or similar component
        self.repeating_panel_1.items = filtered_emis

    def convert_panel_to_pdf(self):
      # Assuming 'content_panel' is the panel containing your data
      content_panel = self.content_panel
      
      # Call the server function to create the PDF from the content panel
      pdf = anvil.server.call('create_pdf_of_payment_receipt', content_panel)
      
      # Prompt the user to download the PDF
      anvil.media.download(pdf)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.accounting.payment_receipt.emi_details', selected_row = self.selected_row)

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.convert_panel_to_pdf()
