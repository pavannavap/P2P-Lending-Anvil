from ._anvil_designer import part_paymentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import main_form_module as main_form_module
from datetime import date


class part_payment(part_paymentTemplate):
  def __init__(self,loan_details,selected_row, **properties):
    self.loan_details = loan_details
    self.selected_row = selected_row
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.loan_id_label.text = loan_details['lender_full_name']
    self.loan_amount_label.text = loan_details['loan_amount']
    self.total_emi_amount_label.text = loan_details['total_emi_amount']
    self.emi_amount_label.text = loan_details['emi_amount']
    self.account_no_label.text = loan_details['account_no']
    self.tenure_label.text = loan_details['tenure']
    self.interest_label.text = loan_details['interest_amount']
    self.remainining_amount.text = loan_details['remainining_amount']
    current_emi_number = loan_details['current_emi_number']
    extra_fee = loan_details['extra_fee']
    prev_next_payment = loan_details['prev_next_payment']
    prev_scheduled_payment = loan_details['prev_scheduled_payment']
    borrower_email = loan_details['borrower_email']
    lender_email = loan_details['lender_email']
    emi_payment_type = loan_details['emi_payment_type']
    
    print(current_emi_number)

    total_emi_amount = float(loan_details['total_emi_amount'])
    half_emi_amount = total_emi_amount / 2
    self.label_6.text = "{:.2f}".format(half_emi_amount)
    self.label_6.enabled = False

    loan_id = self.loan_details['loan_id']
    emi_number = self.loan_details['current_emi_number']
    emi_row = app_tables.fin_emi_table.get(
            loan_id=loan_id,
            emi_number=emi_number + 1
        )

    if emi_row is not None and emi_row['payment_type'] == 'part payment':
            # Now we have the emi_row, proceed with the rest of the code
            part_payment_amount = emi_row['part_payment_amount']
            # total_emi_amount = float(self.total_emi_amount_label.text)

            # # Calculate the remaining amount after deducting the part payment amount
            # remaining_part_payment_amount = total_emi_amount - part_payment_amount

            # Display the remaining amount in the text box
            fee_details = self.calculate_additional_fees(emi_row)
      
            additional_fees = fee_details['total_additional_fees']
            lapsed_fee_amount = fee_details['lapsed_fee_amount']
            default_fee_amount = fee_details['default_fee_amount']
            npa_fee_amount = fee_details['npa_fee_amount']
            
            # Display or use the fee amounts as needed
            print(f"Total Additional Fees: {additional_fees}")
            print(f"Lapsed Fee: {lapsed_fee_amount}")
            print(f"Default Fee: {default_fee_amount}")
            print(f"NPA Fee: {npa_fee_amount}")
      
            if additional_fees is not None:
              part_payment_amount += additional_fees
              if additional_fees > 0:
                self.additional_fee_label.visible = True
                self.additional_fee.visible = True
                self.additional_fee.text ="{:.2f}".format(additional_fees)
            else:
              return part_payment_amount
            self.label_6.text ="{:.2f}".format(part_payment_amount)
            self.label_6.enabled = False
            self.label_3.visible = False
            self.total_emi_amount_label.visible = False


  def pay_now_click(self, **event_args):
      """This method is called when the button is clicked"""
      entered_amount = float(self.label_6.text)  # Get the amount entered by the user
      total_emi_amount = float(self.total_emi_amount_label.text)  # Get the total EMI amount
      loan_id = self.loan_details['loan_id']
      emi_number = self.loan_details['current_emi_number']
      emi_row_1 = app_tables.fin_emi_table.get(
              loan_id=loan_id,
              emi_number=emi_number
          )
      emi_row = app_tables.fin_emi_table.get(
              loan_id=loan_id,
              emi_number=emi_number + 1
          )
  
      # Check if the payment type is 'part payment' and process the payment accordingly
      if emi_row and emi_row['payment_type'] == 'part payment':
          # text_amount = float(self.text_box_1.text)
          fee_details = self.calculate_additional_fees(emi_row)

          additional_fees = fee_details['total_additional_fees']
          lapsed_fee_amount = fee_details['lapsed_fee_amount']
          default_fee_amount = fee_details['default_fee_amount']
          npa_fee_amount = fee_details['npa_fee_amount']
          
          # Display or use the fee amounts as needed
          print(f"Total Additional Fees: {additional_fees}")
          print(f"Lapsed Fee: {lapsed_fee_amount}")
          print(f"Default Fee: {default_fee_amount}")
          print(f"NPA Fee: {npa_fee_amount}")
        
          
          if additional_fees is not None:
            text_amount = emi_row['part_payment_amount'] + additional_fees
          else:
            text_amount = emi_row['part_payment_amount']

          part_payment_date = emi_row['scheduled_payment']
          days_elapsed = self.calculate_date_difference(part_payment_date, datetime.now().date())
          print(days_elapsed)
          borrower_wallet = app_tables.fin_wallet.get(customer_id=self.loan_details['borrower_customer_id'])
          lender_wallet = app_tables.fin_wallet.get(customer_id=self.loan_details['lender_customer_id'])
  
          # Check if borrower and lender wallets exist
          if borrower_wallet and lender_wallet:
              # Check if the borrower's wallet balance is sufficient for the payment
              if borrower_wallet['wallet_amount'] >= text_amount:
                  # Deduct from borrower's wallet
                  borrower_balance = borrower_wallet['wallet_amount']
                  new_borrower_balance = borrower_balance - text_amount
                  borrower_wallet['wallet_amount'] = new_borrower_balance
                  borrower_wallet.update()
  
                  # Add to lender's wallet
                  lender_balance = lender_wallet['wallet_amount']
                  new_lender_balance = lender_balance + text_amount
                  lender_wallet['wallet_amount'] = new_lender_balance
                  lender_wallet.update()
  
                  # Update remaining amount in loan details table
                  remaining_amount = float(self.loan_details['remainining_amount']) - float(self.loan_details['for_remaining_amount_calculation']) /2
                  loan_id = self.loan_details['loan_id']
  
                  loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
                  if loan_row is not None:
                      loan_row['remaining_amount'] = round(remaining_amount ,2)
                      total_paid = float(loan_row['total_amount_paid']) + text_amount
                      loan_row['total_amount_paid'] = total_paid
                      loan_row['lender_returns'] += float(self.loan_details['i_r']) /2
                      if loan_row['remaining_amount'] <= 0:
                        loan_row['loan_updated_status'] = 'closed'
                        
                        lender_data = app_tables.fin_lender.get(customer_id=self.loan_details['lender_customer_id'])
                        if lender_data:
                            lender_data['present_commitments'] -= self.selected_row['loan_amount']
                            lender_data.update()
                      loan_row.update()

                  part_lender_returns = float(self.loan_details['i_r']) /2
                  part_remaining_amount = float(self.loan_details['for_remaining_amount_calculation']) /2

                  # additional_fees = self.calculate_additional_fees(emi_row)

                  existing_fee_rows = app_tables.fin_platform_details.get()
                  if existing_fee_rows is None:
                    app_tables.fin_platform_details.add_row(platform_returns=additional_fees)
                  else:
                    existing_fee_rows['platform_returns'] +=additional_fees
                    existing_fee_rows.update()
                
                  if emi_row:
                      emi_row['payment_type'] = 'pay now'
                      emi_row['part_payment_amount'] -= text_amount
                      emi_row['amount_paid'] += text_amount
                      # emi_row['next_payment'] = next_next_payment
                      emi_row['extra_fee'] += additional_fees
                      emi_row['part_payment_done'] = 2
                      emi_row['lender_returns'] += part_lender_returns
                      emi_row['part_remaining_amount'] += part_remaining_amount
                      emi_row['days_left'] = days_elapsed
                      emi_row['lapsed_fee'] += lapsed_fee_amount
                      emi_row['default_fee'] += default_fee_amount
                      emi_row['lapsed_fee'] += npa_fee_amount
                      emi_row['total_remaining_amount'] = round(remaining_amount ,2)
                      emi_row['total_platform_fee'] +=additional_fees
                      emi_row.update()
  
                  alert("Payment successful!")
                  open_form('borrower.dashboard')
              else:
                  alert("Error: Insufficient balance in the  wallet.")
                  open_form('wallet.wallet')
          else:
              alert("Error: Wallet record not found.")
      else:
          
          if entered_amount <= total_emi_amount:
              # Proceed with the payment process
              borrower_wallet = app_tables.fin_wallet.get(customer_id=self.loan_details['borrower_customer_id'])
              lender_wallet = app_tables.fin_wallet.get(customer_id=self.loan_details['lender_customer_id'])
  
              if borrower_wallet is not None and lender_wallet is not None:
                  # Check if the borrower's wallet balance is sufficient for the payment
                  if borrower_wallet['wallet_amount'] >= entered_amount:
                      # Deduct from borrower's wallet
                      borrower_balance = borrower_wallet['wallet_amount']
                      new_borrower_balance = borrower_balance - entered_amount
                      borrower_wallet['wallet_amount'] = new_borrower_balance
                      borrower_wallet.update()
  
                      # Add to lender's wallet
                      lender_balance = lender_wallet['wallet_amount']
                      new_lender_balance = lender_balance + entered_amount
                      lender_wallet['wallet_amount'] = new_lender_balance
                      lender_wallet.update()

                      total_extra_fee = self.loan_details['total_extra_fee']
                      existing_fee_rows = app_tables.fin_platform_details.get()
                      if existing_fee_rows is None:
                        app_tables.fin_platform_details.add_row(platform_returns=total_extra_fee)
                      else:
                        existing_fee_rows['platform_returns'] +=total_extra_fee
                        existing_fee_rows.update()
                        
                      # Update remaining amount in loan details table
                      remaining_amount = float(self.loan_details['remainining_amount']) - float(self.loan_details['for_remaining_amount_calculation']) /2
                      loan_id = self.loan_details['loan_id']

                      remaining_tenure = float(self.loan_details['remaining_tenure'])
                      print(remaining_tenure)
                      if remaining_tenure != 0:
                        remaining_tenure = remaining_tenure
                        
                      else:
                        remaining_tenure = float(self.loan_details['tenure'])
                        print(remaining_tenure)
                    
                      loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
                      if loan_row is not None:
                          loan_row['remaining_amount'] = round(remaining_amount , 2)
                          if loan_row['total_amount_paid'] is None:
                            loan_row['total_amount_paid'] = 0.0
                            total_paid = loan_row['total_amount_paid'] + entered_amount
                          else:
                            total_paid = loan_row['total_amount_paid'] + entered_amount
                          loan_row['total_amount_paid'] = total_paid
                          # if la
                          if loan_row['lender_returns'] is None:
                            loan_row['lender_returns'] = 0
                          loan_row['lender_returns'] += round(float(self.loan_details['i_r']) /2 ,2)

                          
                          loan_row.update()

                          days_left = self.loan_details['days_left']
                          # Update current_emi_number, next_payment, and add a new row to fin_emi_table
                          current_emi_number = self.loan_details['current_emi_number']
                          extra_fee = self.loan_details['extra_fee']
                          prev_next_payment = self.loan_details['prev_next_payment']
                          prev_scheduled_payment = self.loan_details['prev_scheduled_payment']
                          borrower_email = self.loan_details['borrower_email']
                          lender_email = self.loan_details['lender_email']
                          emi_payment_type = self.loan_details['emi_payment_type']
                          borrower_customer_id = self.loan_details['borrower_customer_id']
                          lender_customer_id = self.loan_details['lender_customer_id']
                          account_no = self.loan_details['account_no']
                          # remaining_tenure = self.loan_details['remaining_tenure']
  
                          # Calculate next_scheduled_payment and next_next_payment based on emi_payment_type
                          if emi_payment_type in ['One Time', 'Monthly', 'Three Months', 'Six Months']:
                              if emi_payment_type == 'Monthly':
                                  remaining_tenure -=1
                                  next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                                  next_next_payment = prev_next_payment + timedelta(days=30)
                              elif emi_payment_type == 'Three Months':
                                  remaining_tenure -=3
                                  next_scheduled_payment = prev_scheduled_payment + timedelta(days=90)
                                  next_next_payment = prev_next_payment + timedelta(days=90)
                              elif emi_payment_type == 'Six Months':
                                  remaining_tenure -=6
                                  next_scheduled_payment = prev_scheduled_payment + timedelta(days=180)
                                  next_next_payment = prev_next_payment + timedelta(days=180)
                              elif emi_payment_type == 'One Time':
                                  if self.loan_details['tenure']:
                                      # next_scheduled_payment = prev_scheduled_payment + timedelta(days=30 * tenure)
                                      # next_next_payment = self.selected_row['next_payment'] + timedelta(days=30 * tenure)
                                      next_scheduled_payment = prev_scheduled_payment + timedelta(days=30 * self.loan_details['tenure'])
                                      next_next_payment = self.selected_row['next_payment'] + timedelta(days=30 * self.loan_details['tenure'])
                          else:
                              # Default to monthly calculation
                              next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                              next_next_payment = prev_next_payment + timedelta(days=30)

                          npa = (self.loan_details['npa_fee'])
                          default = (self.loan_details['default_fee'])
                          lapsed = (self.loan_details['lapsed_fee'])
                          lender_returns_in_emi_table = float(self.loan_details['i_r']) /2
                          remaining_amount_in_emi_table = float(self.loan_details['for_remaining_amount_calculation']) /2
                          # Add a new row to fin_emi_table
                          new_emi_row = app_tables.fin_emi_table.add_row(
                              loan_id=loan_id,
                              emi_number=current_emi_number + 1,
                              account_number=account_no,
                              scheduled_payment_made=datetime.now(),
                              scheduled_payment=next_scheduled_payment,
                              next_payment=next_next_payment,
                              amount_paid=entered_amount,
                              extra_fee=extra_fee,
                              borrower_customer_id=borrower_customer_id,
                              lender_customer_id=lender_customer_id,
                              borrower_email=borrower_email,
                              lender_email=lender_email,
                              payment_type='part payment',
                              part_payment_date=datetime.today().date(),
                              part_payment_amount=total_emi_amount - entered_amount,
                              part_payment_done= 1,
                              total_amount_pay= float(self.loan_details['total_emi_amount']),
                              remaining_tenure=remaining_tenure,
                              lender_returns=lender_returns_in_emi_table,
                              part_remaining_amount=remaining_amount_in_emi_table,
                              days_left=days_left,
                              npa_fee=npa,
                              default_fee=default,
                              lapsed_fee=lapsed,
                              total_remaining_amount=round(remaining_amount , 2),
                              total_platform_fee=total_extra_fee,
                            
                              
                              
                          )
  
                          # Update the emi_number and next_payment in the loan_details
                          self.loan_details['emi_number'] = current_emi_number + 1
                          self.loan_details['next_payment'] = next_next_payment
                          self.loan_details.update()
  
                      alert("Payment successful!")
                      open_form('borrower.dashboard')
                  else:
                      alert("Error: Insufficient balance in the  wallet.")
                      open_form('wallet.wallet')
              else:
                  alert("Error: Wallet record not found.")
          else:
              # Show an alert if the entered amount is greater than the total EMI amount
              alert("Entered amount exceeds the total EMI amount. Please enter a valid amount.")
  
  def calculate_date_difference(self,date_to_subtract, today_date):
    return (today_date - date_to_subtract).days
    print ((today_date - date_to_subtract).days)

  def calculate_additional_fees(self, emi_row):
        # Retrieve the part_payment_date from emi_row
        part_payment_date = emi_row['scheduled_payment']
        print(part_payment_date)
        

        # Calculate the difference in days between part_payment_date and today's date
        days_elapsed = self.calculate_date_difference(part_payment_date, datetime.now().date())
        print(days_elapsed)

        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        # Fetch necessary fee details based on loan state status and product ID
        product_id = self.loan_details['product_id']
        # loan_state_status = self.loan_details['loan_state_status']
        product_details = app_tables.fin_product_details.get(product_id=product_id)

        # Initialize total additional fees
        total_additional_fees = 0
        lapsed_fee = 0
        default_fee = 0
        npa_fee = 0

        # Check loan state status and calculate additional fees accordingly
        if lapsed_settings :
            lapsed_start = lapsed_settings['minimum_days']  # Assuming column1 stores the start day
            lapsed_end = lapsed_settings['maximum_days']
            if  lapsed_start < days_elapsed <= lapsed_end:
                days_elapsed -= lapsed_start
                lapsed_fee_percentage = product_details['lapsed_fee']
                total_additional_fees += days_elapsed * (lapsed_fee_percentage * float(self.loan_details['emi']) / 100)
                lapsed_fee += days_elapsed * (lapsed_fee_percentage * float(self.loan_details['emi']) / 100)
                print(total_additional_fees)
                print(self.loan_details['emi'])

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
                  lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.loan_details['emi']) / 100)
                  default_fee_amount += lapsed_fee_amount
  
              if product_details['default_fee'] != 0:
                  default_fee_percentage = product_details['default_fee']
                  default_fee_amount += days_in_default * (default_fee_percentage * float(self.loan_details['emi']) / 100)
              elif product_details['default_fee_amount'] != 0:
                  default_fee_amount += days_in_default * product_details['default_fee_amount']
              
              total_additional_fees += default_fee_amount
              default_fee += default_fee_amount
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
                  lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.loan_details['emi']) / 100)
                  npa_fee_amount += lapsed_fee_amount
  
              # Include default end fee if applicable
              if default_settings and days_elapsed > default_end:
                  days_in_default = default_end - default_start
                  if product_details['default_fee'] != 0:
                      default_fee_percentage = product_details['default_fee']
                      default_fee_amount = days_in_default * (default_fee_percentage * float(self.loan_details['emi']) / 100)
                      npa_fee_amount += default_fee_amount
                  elif product_details['default_fee_amount'] != 0:
                      default_fee_amount = days_in_default * product_details['default_fee_amount']
                      npa_fee_amount += default_fee_amount
  
              if product_details['npa'] != 0:
                  npa_fee_percentage = product_details['npa']
                  npa_fee_amount += days_in_npa * (npa_fee_percentage * float(self.loan_details['emi']) / 100)
              elif product_details['npa_amount'] != 0:
                  npa_fee_amount += days_in_npa * product_details['npa_amount']
              
              total_additional_fees += npa_fee_amount
              npa_fee += npa_fee_amount
              print(f"NPA Fee: {npa_fee_amount}")


        fee_details = {
        "total_additional_fees": total_additional_fees,
        "lapsed_fee_amount": lapsed_fee,
        "default_fee_amount": default_fee,
        "npa_fee_amount": npa_fee
    }
        print(f"Total Additional Fees: {total_additional_fees}")
        return fee_details

  def button_1_copy_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard.today_dues.check_out',self.selected_row)

            

 
