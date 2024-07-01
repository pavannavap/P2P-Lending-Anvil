from ._anvil_designer import borrower_extensionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta



class borrower_extension(borrower_extensionTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.selected_row = selected_row
        # self.label_loan_id.text = f"{selected_row['loan_id']}"
        self.label_name.text = f"{selected_row['borrower_full_name']}"
        self.label_loan_amount.text = f"{selected_row['loan_amount']}"
        self.label_loan_tenure.text = f"{selected_row['tenure']} Months"
        self.label_interest_rate.text = f"{selected_row['interest_rate']} % pa"  
        self.label_5_copy.text = "Loan Extension Request is Under Process..."
        self.label_5_copy_2.text = "Loan Extension Request is Accepted"
        self.label_5_copy_3.text = "Loan Extension Request is Rejected"
        product_id_to_search = selected_row['product_id']
        data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
        self.foreclosure_type_lst = [] 
        self.extension_fee_lst = []
        for i in data:
            self.foreclosure_type_lst.append(i['extension_allowed'])
            self.extension_fee_lst.append(i['extension_fee'])
        
        self.extension_allow.text = self.foreclosure_type_lst[0]
        self.extension_fee.text = self.extension_fee_lst[0]

        loan_id = selected_row['loan_id']
        loan_details_row = app_tables.fin_loan_details.get(loan_id=loan_id)
      
        # Check status for the selected loan ID
        loan_id = selected_row['loan_id']
        extend_rows = app_tables.fin_extends_loan.search(loan_id=loan_id)

        if extend_rows:
          for extend_row in extend_rows :
            if extend_row['status'] not in ('approved', 'rejected'):
              approval_days_row = app_tables.fin_approval_days.get(loans='Extension')
            
              if approval_days_row:
                  approval_days = approval_days_row['days_for_approval']
                  
                  # Calculate the time difference between now and the request date
                  print("Extension Request Date:", extend_row['extension_request_date'])
                  time_difference = datetime.now() - datetime.combine(extend_row['extension_request_date'], datetime.min.time())
                  print("Time Difference (seconds):", time_difference.total_seconds())
      
                  # Check if the time difference is more than the approval days
                  if time_difference.total_seconds() > (approval_days * 86400):  # 86400 seconds in a day
                      extend_row['status'] = 'approved'
                      extend_row['status_timestamp '] = datetime.now()
                      extend_row.update()

      
        extend_rows = app_tables.fin_extends_loan.search(loan_id=loan_id)

        approved_status = False
        rejected_status = False

        for row in extend_rows:
            if row['status'] == 'approved':
                approved_status = True
                break
            elif row['status'] == 'rejected':
                rejected_status = True
                break

        if approved_status:
            # If there is an approved status, make "Pay" button visible
            self.label_5_copy_2.visible = True
            self.button_1_copy.visible = False 
            self.button_s.visible = True
            self.button_1.visible = False
            self.button_2.visible = False
            loan_details_row = loan_details_row['loan_extension_months']
            self.text_box_1.text = str(loan_details_row)
            Notification("Your request has been accepted.").show()
        elif rejected_status:
            # If there is a reject status, show an alert            
            self.label_5_copy_3.visible = True
            self.button_1_copy.visible = False 
            self.button_s.visible = True
            self.button_1.visible = False
            self.button_2.visible = False
            loan_details_row = loan_details_row['loan_extension_months']
            self.text_box_1.text = str(loan_details_row)
            Notification('Your request has been rejected.').show()
        else:
            # If there is no approved or reject status, check if the loan ID is in extend loan table
            existing_requests = app_tables.fin_extends_loan.search(loan_id=loan_id)
            if len(existing_requests) == 0:
                # If the loan ID is not in the foreclosure table, make "Foreclose" button and button2 visible                
                self.button_2.visible = True
                self.button_1_copy.visible = True
                self.button_s.visible = False
                self.button_1.visible = False
            else:
                loan_details_row = loan_details_row['loan_extension_months']
                self.text_box_1.text = str(loan_details_row)
                self.button_2.visible = False 
                self.label_5_copy.visible = True
                self.button_1_copy.visible = False 
                self.button_s.visible = True
                self.button_1.visible = False
            
            # Fetch scheduled payments from fin_emi_table
        self.selected_row = selected_row
  
        product_id = selected_row['product_id']
        product_details_row = app_tables.fin_product_details.get(product_id=product_id)
        self.min_months = product_details_row['min_extension_months']
        self.min_months = int(self.min_months)

        loan_id = selected_row['loan_id']
        # Fetching the last row data for the specified loan_id from the fin_emi_table
        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id)
        if last_emi_rows:
    # Convert LiveObjectProxy to list
            last_emi_list = list(last_emi_rows)
            
            if last_emi_list:
                # Sort the list of rows based on the 'emi_number' column in reverse order
                last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)
                
                # Extract the 'emi_number' from the first row, which represents the highest 'emi_number'
                total_payments_made = last_emi_list[0]['emi_number']
            else:
                total_payments_made = 0
        else:
            total_payments_made = 0

        print("total payment made", total_payments_made)
        # Set the label text
        # self.label_tpm.text = f"{total_payments_made} months"
        self.total_payments_made = total_payments_made
            
            # Check if there are scheduled payments within 2 days before the due date
            # today = datetime.now().date()
            # scheduled_payment_found = any(
            #     (emi_row['scheduled_payment'] - today).days <= 2
            #     for emi_row in emi_rows if emi_row['scheduled_payment'] is not None
            # )
            
            # # Update visibility based on scheduled payments
            # self.button_2.visible = self.button_2.visible and not scheduled_payment_found
            # self.button_1.visible = self.button_1.visible and scheduled_payment_found
            
            # # Additional condition to make button_1 visible if there are no existing requests
            # if len(existing_requests) == 0:
            #     self.button_1_copy.visible = True
    
    def button_1_click(self, **event_args):
        """This method is called when the Back button is clicked"""
        open_form('borrower.dashboard.extension_loan_request')

    def button_s_click(self, **event_args):
        """This method is called when the Close button is clicked"""
        open_form('borrower.dashboard.extension_loan_request')

    def button_2_click(self, **event_args):
        """This method is called when the Submit Extension Request button is clicked"""
        # Validate extension months before allowing the borrower to proceed
        if self.total_payments_made >=self.min_months:
        
        
          if self.validate_extension_months():
              # Get the loan_id and extension months
              loan_id = self.selected_row['loan_id']
              loan_extension_months = int(self.text_box_1.text.strip())
  
              # Check if a row with the specified loan_id already exists in loan_details
              existing_row = app_tables.fin_loan_details.get(loan_id=loan_id)
  
              if existing_row is not None:
                  # Update the existing row
                  existing_row.update(loan_extension_months=loan_extension_months)
              else:
                  # Create a new row
                  app_tables.fin_loan_details.add_row(
                      loan_id=loan_id,
                      loan_extension_months=loan_extension_months
                  )
              extension_fee_percentage = float(self.extension_fee.text)
            
              # Close the current form or navigate to another form if needed
              open_form('borrower.dashboard.extension_loan_request.payment_details_extension', selected_row=self.selected_row, loan_extension_months=loan_extension_months, extension_fee=extension_fee_percentage)
        else:
          alert(alert('You are not eligible for Extension! You have to pay at least ' + str(self.min_months) + ' months.'))
          open_form('borrower.dashboard.extension_loan_request')
          
    def validate_extension_months(self):
        """Validate the extension months entered by the borrower"""
        extension_months = self.text_box_1.text.strip()

        if extension_months and extension_months.isdigit():
            loan_extension_months = int(extension_months)
            if 0 < loan_extension_months <= 6:
                return True
            else:
                alert("Extension months must be between 1 and 6.", title="Validation Error")
        else:
            alert("Please enter a valid number of extension months.", title="Validation Error")
        
        return False

    def button_1_copy_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('borrower.dashboard.extension_loan_request')








