from ._anvil_designer import borrower_foreclosureTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime ,timedelta
import sys as sys

class borrower_foreclosure(borrower_foreclosureTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # self.label_loan_id.text = f"{selected_row['loan_id']}"
        self.label_name.text = f"{selected_row['borrower_full_name']}"
        self.label_loan_amount.text = f"{selected_row['loan_amount']}"
        self.label_loan_tenure.text = f"{selected_row['tenure']} Months"
        self.label_interest_rate.text = f"{selected_row['interest_rate']} % pa"
        self.label_credit_limit.text = f"{selected_row['credit_limit']}"
        self.label_3.text = "Foreclosure Request Under Process......"  
        self.label_5.text = "Foreclosure Request Rejected"
        self.label_8.text = "Foreclosure is not available for this product.."
        product_id_to_search = selected_row['product_id']
        data = tables.app_tables.fin_product_details.search(product_id=product_id_to_search)
        self.foreclosure_type_lst = []    
        for i in data:
            self.foreclosure_type_lst.append(i['foreclose_type'])
        
        self.foreclose_type.text = self.foreclosure_type_lst[0]
        print(self.foreclose_type.text)

        # Check status for the selected loan ID
        loan_id = selected_row['loan_id']
        foreclosure_rows = app_tables.fin_foreclosure.search(loan_id=loan_id)

        if foreclosure_rows:
          for extend_row in foreclosure_rows :
            if extend_row['status'] not in ('approved', 'rejected'):
              approval_days_row = app_tables.fin_approval_days.get(loans='Extension')
            
              if approval_days_row:
                  approval_days = approval_days_row['days_for_approval']
                  
                  # Calculate the time difference between now and the request date
                  print("Extension Request Date:", extend_row['requested_on'])
                  time_difference = datetime.now() - datetime.combine(extend_row['requested_on'], datetime.min.time())
                  print("Time Difference (seconds):", time_difference.total_seconds())
      
                  # Check if the time difference is more than the approval days
                  if time_difference.total_seconds() > (approval_days * 86400):  # 86400 seconds in a day
                      extend_row['status'] = 'approved'
                      extend_row['status_timestamp '] = datetime.now()
                      extend_row.update()

      
        foreclosure_rows = app_tables.fin_foreclosure.search(loan_id=loan_id)

        approved_status = False
        rejected_status = False

        for row in foreclosure_rows:
            if row['status'] == 'approved':
                approved_status = True
                break
            elif row['status'] == 'rejected':
                rejected_status = True
                break

        if approved_status:
            # If there is an approved status, make "Pay" button visible
            self.button_foreclose.visible = False
            self.button_2.visible = False
            self.button_3.visible = True
            self.button_4.visible = True

            self.foreclose_amount.visible = True
            self.label_11.visible = True
            self.label_14.visible = True
            self.label_17.visible = True
            self.due_amount.visible = True
            self.total_amount.visible = True

            # foreclosure_row = app_tables.fin_foreclosure.get(loan_id=loan_id)
            # if foreclosure_row :
            #   foreclosure_amount = foreclosure_row['foreclose_amount']
            #   total_due_amount =foreclosure_row['total_due_amount']
            #   total_amount = foreclosure_amount  + total_due_amount
            #   self.foreclose_amount.text ="{:.2f}".format(foreclosure_amount)
            #   self.due_amount.text ="{:.2f}".format(total_due_amount)
            #   self.total_amount.text ="{:.2f}".format(total_amount)

              
            Notification("Your request has been accepted.").show()
        elif rejected_status:
            # If there is a reject status, show an alert
            Notification('Your request has been rejected.').show()
            self.button_foreclose.visible = False
            self.button_2.visible = False
            self.button_3.visible = False
            self.label_5.visible = True
            self.button_5.visible = False
            self.foreclose_again.visible = True
            self.foreclose_back.visible = True
        else:
            # If there is no approved or reject status, check if the loan ID is in foreclosure table
            existing_requests = app_tables.fin_foreclosure.search(loan_id=loan_id)
            if len(existing_requests) == 0 and self.foreclose_type.text != "Not Eligible":
                # If the loan ID is not in the foreclosure table, make "Foreclose" button and button2 visible
                self.button_foreclose.visible = True
                self.button_2.visible = True
                self.button_3.visible = False
                self.button_4.visible = False
            elif self.foreclose_type.text == "Not Eligible":
                # If the loan ID is in the foreclosure table, make other buttons visible
                self.button_foreclose.visible = False
                self.button_2.visible = False 
                self.button_4.visible = False
                self.button_3.visible = False
                self.label_8.visible = True
                self.button_5.visible = True
            else:
                self.button_foreclose.visible = False
                self.button_2.visible = False 
                self.button_4.visible = False
                self.button_3.visible = False
                self.label_3.visible = True
                self.button_5.visible = True

        # Save selected_row as an instance variable for later use
        self.selected_row = selected_row
  
        product_id = selected_row['product_id']
        product_details_row = app_tables.fin_product_details.get(product_id=product_id)
        self.min_months = product_details_row['min_months']
        self.min_months = int(self.min_months)

        loan_id = selected_row['loan_id']
        # Fetching the last row data for the specified loan_id from the fin_emi_table
        last_emi_rows = app_tables.fin_emi_table.search(loan_id=loan_id)
        try:
            if last_emi_rows:
                # Convert LiveObjectProxy to list
                last_emi_list = list(last_emi_rows)
                
                if last_emi_list:
                    # Sort the list of rows based on the 'emi_number' column in reverse order
                    last_emi_list.sort(key=lambda x: x['emi_number'], reverse=True)
                    
                    # Extract the 'emi_number' from the first row, which represents the highest 'emi_number'
                    total_payments_made = last_emi_list[0]['emi_number']
                    
                    print("Total payment made:", total_payments_made)
                    # Set the label text
                    self.label_tpm.text = f"{total_payments_made} months"
                    self.total_payments_made = total_payments_made

                    next_payment_date = last_emi_list[0]['next_payment']
                    if next_payment_date:
                        if (next_payment_date - timedelta(days=2)) > datetime.now().date():
                            self.is_payment_date_valid = True

                            # foreclosure_row = app_tables.fin_foreclosure.get(loan_id=loan_id)
                            # if foreclosure_row:
                            #     foreclosure_amount = foreclosure_row['foreclose_amount']
                            #     total_due_amount = foreclosure_row['total_due_amount']
                            #     total_amount = foreclosure_amount + total_due_amount
                            #     self.foreclose_amount.text = "{:.2f}".format(foreclosure_amount)
                            #     self.due_amount.text = "{:.2f}".format(total_due_amount)
                            #     self.total_amount.text = "{:.2f}".format(total_amount)
                              
                            #     emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=total_payments_made)
                            #     if emi_row:
                            #           next_payment_date = emi_row['next_payment']
                            #         # if next_payment_date  < (datetime.now()):
                            #           additional_fees = self.calculate_additional_fees(emi_row)
                            #           if additional_fees is not None:
                            #               # total_amount = float(self.total_amount.text)
                            #               total_amount += additional_fees
                            #               if additional_fees > 0:
                            #                   self.label_13.visible = True
                            #                   self.extra_fee.visible = True
                            #                   self.extra_fee.text = "{:.2f}".format(additional_fees)
                            #                   self.total_amount.text = "{:.2f}".format(total_amount)
                            #               else:
                            #                 self.extra_fee.text = 0

                      

                      
                        else:
                            self.is_payment_date_valid = False
                            # alert("The next payment date must be at least two days before today's date for foreclosure.")
                    else:
                        self.is_payment_date_valid = False
                        alert("Next payment date not found.")
                        open_form('borrower.dashboard.foreclosure_request')
                else:
                    total_payments_made = 0
                    self.label_tpm.text = 0
                    self.button_2.visible = False
                    self.button_foreclose.visible = False
                    self.button_5.visible = True
                    # self.label_tpm.text = 0
                    alert("No EMIs found for this loan.") 
                    open_form('borrower.dashboard')
            else:
                total_payments_made = 0
                # self.label_tpm.text = 0
                alert("No EMIs found for this loan.")   
                # open_form('borrower.dashboard')
        except ValueError as e:
            alert(str(e))
            
            
        foreclosure_row = app_tables.fin_foreclosure.get(loan_id=loan_id)
        if foreclosure_row:
                                foreclosure_amount = foreclosure_row['foreclose_amount']
                                total_due_amount = foreclosure_row['total_due_amount']
                                total_amount = foreclosure_amount + total_due_amount
                                self.foreclose_amount.text = "{:.2f}".format(foreclosure_amount)
                                self.due_amount.text = "{:.2f}".format(total_due_amount)
                                self.total_amount.text = "{:.2f}".format(total_amount)
                              
                                emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=total_payments_made)
                                if emi_row:
                                      next_payment_date = emi_row['next_payment']
                                    # if next_payment_date  < (datetime.now()):
                                      additional_fees = self.calculate_additional_fees(emi_row)
                                      if additional_fees is not None:
                                          # total_amount = float(self.total_amount.text)
                                          total_amount += additional_fees
                                          if additional_fees > 0:
                                              self.label_13.visible = True
                                              self.extra_fee.visible = True
                                              self.extra_fee.text = "{:.2f}".format(additional_fees)
                                              self.total_amount.text = "{:.2f}".format(total_amount)
                                          else:
                                            self.extra_fee.text = 0

                      
        # emi_row = app_tables.fin_emi_table.get(loan_id=loan_id,emi_number = total_payments_made)
        # if emi_row :
        #         next_payment_date = emi_row['next_payment']
        #       # if next_payment_date  < (datetime.now()):
        #         additional_fees = self.calculate_additional_fees(emi_row)
        #         if additional_fees is not None:
        #           total_amount += additional_fees
        #           if additional_fees > 0:
        #             self.label_13.visible = True
        #             self.extra_fee.visible = True
        #             self.extra_fee.text ="{:.2f}".format(additional_fees)
        #             self.total_amount.text ="{:.2f}".format(total_amount)
        
    def button_foreclose_click(self, **event_args):
        selected_row = self.selected_row
        # loan_id = selected_row['loan_id']
        # total_payments_made = self.loan_details_row['total_payments_made']
        if self.total_payments_made >= self.min_months and self.is_payment_date_valid:
            open_form('borrower.dashboard.foreclosure_request.borrower_foreclosure.foreclose', selected_row=selected_row, total_payments_made=self.total_payments_made)
        else:
            if not self.is_payment_date_valid:
                alert('The next payment date must be at least two days before today\'s date for foreclosure.')
            else:
                alert('You are not eligible for foreclosure! You have to pay at least ' + str(self.min_months) + ' months.')
            open_form('borrower.dashboard.foreclosure_request')

  
    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard.foreclosure_request')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard')

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard.foreclosure_request')

    def button_5_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard.foreclosure_request')

    def foreclose_again_click(self, **event_args):
        """This method is called when the button is clicked"""
        loan_id = self.selected_row['loan_id']
    
        # Search for the corresponding row in the fin_foreclosure table
        foreclosure_row = app_tables.fin_foreclosure.get(loan_id=loan_id)
        
        # Update the status to "Under Process"
        foreclosure_row['status'] = 'under process'
        
        # Update the requested_on column with today's date and time
        foreclosure_row['requested_on'] = datetime.now()
        
        # Save the changes
        foreclosure_row.update()
        alert("Your Foreclosure request is submitted.")
        open_form('borrower.dashboard')


    def again_back_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('borrower.dashboard.foreclosure_request')

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        selected_row = self.selected_row
        loan_id = selected_row['loan_id']
        borrower_id = selected_row['borrower_customer_id']
        lender_id = selected_row['lender_customer_id']
        borrower_email_id = selected_row['borrower_email_id']
        lender_email_id = selected_row['lender_email_id']

        # Fetch the foreclosure row
        foreclosure_row = app_tables.fin_foreclosure.get(loan_id=loan_id)
        if not foreclosure_row:
            alert("Foreclosure details not found.")
            return

        extra_fee = float(self.extra_fee.text)
        if extra_fee  is None:
          extra_fee = 0.0
        
          
        foreclosure_amount = foreclosure_row['foreclose_amount']
        total_due_amount = foreclosure_row['total_due_amount']
        total_amount =  total_due_amount + extra_fee
        total_extra_fee = foreclosure_amount + float(self.extra_fee.text)

        # self.foreclose_amount.text ="{:.2f}".format(foreclosure_amount)
        # self.due_amount.text ="{:.2f}".format(total_due_amount)
        # self.total_amount.text ="{:.2f}".format(total_amount)

        # Fetch borrower and lender wallets
        borrower_wallet = app_tables.fin_wallet.get(customer_id=borrower_id)
        lender_wallet = app_tables.fin_wallet.get(customer_id=lender_id)

        if borrower_wallet and lender_wallet:
            if borrower_wallet['wallet_amount'] >= total_amount:
                # Deduct from borrower's wallet
                borrower_wallet['wallet_amount'] -= total_amount
                borrower_wallet.update()

                # Add to lender's wallet
                lender_wallet['wallet_amount'] += total_amount
                lender_wallet.update()

                # Update remaining amount in loan details
                loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
                if loan_row:
                    loan_row['remaining_amount'] = 0
                    loan_row['total_amount_paid'] += total_amount
                    loan_row['lender_returns'] += foreclosure_amount
                    loan_row['loan_updated_status'] = 'closed'

                    remaining_amount = 0
                    lender_data = app_tables.fin_lender.get(customer_id=loan_row['lender_customer_id'])
                    if lender_data:
                            lender_data['present_commitments'] -= loan_row['loan_amount']
                            lender_data.update()
                    loan_row.update()


                existing_fee_rows = app_tables.fin_platform_details.get()
                if existing_fee_rows is None:
                  app_tables.fin_platform_details.add_row(platform_returns=total_extra_fee)
                else:
                  existing_fee_rows['platform_returns'] +=total_extra_fee
                  existing_fee_rows.update()
              
                app_tables.fin_emi_table.add_row(
                    loan_id=loan_id,
                    emi_number=self.total_payments_made + 1,  # Assuming the next EMI number
                    scheduled_payment_made=datetime.now(),
                    extra_fee =total_extra_fee,
                    borrower_customer_id=borrower_id,
                    lender_customer_id=lender_id,
                    amount_paid= total_amount,
                    payment_type='Foreclosure',
                    lender_email= lender_email_id,
                    borrower_email= borrower_email_id,
                    total_remaining_amount=remaining_amount,
                    total_platform_fee=total_extra_fee,
                    lender_returns=foreclosure_amount,
           
                )
                Notification("Foreclosure payment completed successfully.").show()
                open_form('borrower.dashboard')
            else:
                alert("Insufficient balance in borrower's wallet.")
                open_form('wallet.wallet')
        else:
            alert("Borrower or lender wallet not found.")







    def calculate_date_difference(self,date_to_subtract, today_date):
      return (today_date - date_to_subtract).days
      print ((today_date - date_to_subtract).days)

    def calculate_additional_fees(self, emi_row):
        # Retrieve the part_payment_date from emi_row
        part_payment_date = emi_row['next_payment']
        print(part_payment_date)

        # Calculate the difference in days between part_payment_date and today's date
        days_elapsed = self.calculate_date_difference(part_payment_date, datetime.now().date())
        print(days_elapsed)

        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        # Fetch necessary fee details based on loan state status and product ID
        selected_row = self.selected_row
  
        product_id = selected_row['product_id']
        # product_details_row = app_tables.fin_product_details.get(product_id=product_id)
        # loan_state_status = self.loan_details['loan_state_status']
        product_details = app_tables.fin_product_details.get(product_id=product_id)

        # Initialize total additional fees
        total_additional_fees = 0

        # Check loan state status and calculate additional fees accordingly
        if lapsed_settings :
            lapsed_start = lapsed_settings['minimum_days']  # Assuming column1 stores the start day
            lapsed_end = lapsed_settings['maximum_days']
            if  lapsed_start < days_elapsed <= lapsed_end:
                days_elapsed -= lapsed_start
                lapsed_fee_percentage = product_details['lapsed_fee']
                total_additional_fees += days_elapsed * (lapsed_fee_percentage * float(self.due_amount.text) / 100)
                print(total_additional_fees)
                # print(self.loan_details['emi'])

        if default_settings:
            default_start = default_settings['minimum_days']
            default_end = default_settings['maximum_days']
            if default_start < days_elapsed <= default_end:
                days_in_default = days_elapsed - default_start
                default_fee_amount = 0
    
                # Include lapsed end fee if applicable
                if lapsed_settings and days_elapsed > lapsed_end:
                    days_in_lapsed = lapsed_end - lapsed_start
                    lapsed_fee_percentage = product_details['lapsed_fee']
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage *float(self.due_amount.text)  / 100)
                    default_fee_amount += lapsed_fee_amount
    
                if product_details['default_fee'] != 0:
                    default_fee_percentage = product_details['default_fee']
                    default_fee_amount += days_in_default * (default_fee_percentage * float(self.due_amount.text) / 100)
                elif product_details['default_fee_amount'] != 0:
                    default_fee_amount += days_in_default * product_details['default_fee_amount']
                
                total_additional_fees += default_fee_amount
                print(f"Default Fee: {default_fee_amount}")

        if npa_settings:
            npa_start = npa_settings['minimum_days']
            npa_end = npa_settings['maximum_days']
            if npa_start < days_elapsed <= npa_end:
                days_in_npa = days_elapsed - npa_start
                npa_fee_amount = 0
    
                # Include lapsed end fee if applicable
                if lapsed_settings and days_elapsed > lapsed_end:
                    days_in_lapsed = lapsed_end - lapsed_start
                    lapsed_fee_percentage = product_details['lapsed_fee']
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage *float(self.due_amount.text) / 100)
                    npa_fee_amount += lapsed_fee_amount
    
                # Include default end fee if applicable
                if default_settings and days_elapsed > default_end:
                    days_in_default = default_end - default_start
                    if product_details['default_fee'] != 0:
                        default_fee_percentage = product_details['default_fee']
                        default_fee_amount = days_in_default * (default_fee_percentage * float(self.due_amount.text) / 100)
                        npa_fee_amount += default_fee_amount
                    elif product_details['default_fee_amount'] != 0:
                        default_fee_amount = days_in_default * product_details['default_fee_amount']
                        npa_fee_amount += default_fee_amount
    
                if product_details['npa'] != 0:
                    npa_fee_percentage = product_details['npa']
                    npa_fee_amount += days_in_npa * (npa_fee_percentage * float(self.due_amount.text) / 100)
                elif product_details['npa_amount'] != 0:
                    npa_fee_amount += days_in_npa * product_details['npa_amount']
                
                total_additional_fees += npa_fee_amount
                print(f"NPA Fee: {npa_fee_amount}")
    
        print(f"Total Additional Fees: {total_additional_fees}")
        return total_additional_fees



