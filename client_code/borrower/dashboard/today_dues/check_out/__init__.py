from ._anvil_designer import check_outTemplate
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
from ...Module1 import transfer_money_1
from collections import defaultdict



class check_out(check_outTemplate):
    def __init__(self, selected_row, **properties):
        self.selected_row = selected_row
        self.user_id = main_form_module.userId
        self.init_components(**properties)
  
        loan_id = selected_row['loan_id']
        remaining_amount = selected_row['remaining_amount']
        
        total_paid_amount = selected_row['total_amount_paid']
        extension_months = self.get_extension_details(loan_id, selected_row['emi_number'])
        extension_amount = self.get_extension_details_1(loan_id,selected_row['emi_number'])
        loan_amount = selected_row['loan_amount']
        tenure = selected_row['tenure'] + extension_months
        interest_rate = selected_row['interest_rate']
        emi_payment_type = selected_row['emi_payment_type']
        total_interest_amount = selected_row['total_interest_amount']
        total_processing_fee_amount = selected_row['total_processing_fee_amount']
        processing_fee = total_processing_fee_amount/ tenure
        # self.processing_fee.text = "{:.2f}".format(processing_fee)
        monthly_interest_rate = interest_rate / 12 / 100
        total_payments = tenure * 12
        total_repayment_amount = selected_row['total_repayment_amount']
        total_i_a = total_interest_amount / tenure

        remaining_tenure = selected_row['remaining_tenure'] + extension_months
        if remaining_tenure == 0:
          remaining_tenure = tenure
          
        if remaining_amount is None:
          remaining_amount = selected_row['total_repayment_amount']
          self.remainining_amount.text = "{:.2f}".format(total_repayment_amount)
        else:
          self.remainining_amount.text =  "{:.2f}".format(remaining_amount)
      
        if emi_payment_type == 'One Time':
            emi = total_repayment_amount
            remaining_tenure = 0
            interest_amount = total_interest_amount
            #total_emi += emi  # Add extension amount to 12-month EMI total
            total_emi = emi +  extension_amount + total_processing_fee_amount
        elif emi_payment_type == 'Monthly':
            # Calculate monthly EMI amount
            if remaining_tenure == 1:
              emi = remaining_amount
              remaining_tenure = 0
              # interest_amount = 0
              processing_fee = 0
              # ending_monthly_interest = total_i_a 
            else:
              remaining_tenure -= 1 
              emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
            interest_amount = total_i_a
            total_emi = emi + extension_amount + processing_fee  # Add extension amount to monthly EMI
        elif emi_payment_type == 'Three Months':
            # Calculate EMI amount for 3 months
            if remaining_tenure < 3:
              emi = remaining_amount
              # ending_monthly_interest = total_i_a * remaining_tenure
              remaining_tenure = 0
              # interest_amount = 0
              processing_fee = 0
            elif remaining_tenure == 3:
              emi = remaining_amount
              remaining_tenure = 0
              # interest_amount = 0
              processing_fee = 0
              # ending_monthly_interest = total_i_a * 3
            else:
              remaining_tenure -= 3 
              emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
              emi*=3
            # Calculate EMI amount for 3 months
              # interest_amount = total_i_a * 3
              processing_fee = processing_fee * 3
            interest_amount = total_i_a * 3
            total_emi = emi + extension_amount + processing_fee # Add extension amount to 3-month EMI
        elif emi_payment_type == 'Six Months':
            if remaining_tenure < 6:
              emi = remaining_amount
              # ending_monthly_interest = total_i_a * remaining_tenure
              remaining_tenure = 0
              # interest_amount = 0
              processing_fee = 0
            elif remaining_tenure == 6:
              emi = remaining_amount
              # ending_monthly_interest = total_i_a * remaining_tenure
              remaining_tenure = 0
              # interest_amount = 0
              processing_fee = 0
            else:
              remaining_tenure -= 6 
              emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
              emi*=6
            # Calculate EMI amount for 3 months
              # interest_amount = total_i_a * 6
              processing_fee = processing_fee * 6

            print(processing_fee)
            print(extension_amount)
            print(emi)
            interest_amount = total_i_a * 6
            total_emi = emi + extension_amount+ processing_fee  # Add extension amount to 6-month EMI
        else:
            # Default to monthly calculation
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount + processing_fee # Add extension amount to monthly EMI

        self.processing_fee.text = "{:.2f}".format(processing_fee)
        self.i_r.text = "{:.2f}".format(interest_amount)
        self.emi.text = "{:.2f}".format(emi)
        self.emi_processing_extension.text = "{:.2f}".format( emi + processing_fee)
        print(float(self.emi.text))
        self.remaining_tenure.text = remaining_tenure
      
        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        
        days_left = selected_row['days_left']
        product_id = selected_row['product_id']        
        # Initialize variables for different fees
        total_lapsed_amount = 0
        total_default_fee = 0
        total_npa_fee = 0
        
        if lapsed_settings:
            lapsed_start = lapsed_settings['minimum_days']
            lapsed_end = lapsed_settings['maximum_days']
            if lapsed_start < days_left <= lapsed_end:
                lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                days_difference = days_left - lapsed_start
                total_lapsed_amount = days_difference * (lapsed_fee_percentage * emi / 100)
                total_emi += total_lapsed_amount
                self.lapsed.text = "{:.2f}".format(total_lapsed_amount)
                self.lapsed.visible = True
                self.label_5.visible = True
                self.default.visible = False
                self.label_9.visible = False
        
        if default_settings:
            default_start = int(default_settings['minimum_days'])
            default_end = int(default_settings['maximum_days'])
            if default_start < days_left <= default_end:
                product_details = app_tables.fin_product_details.get(product_id=product_id)
                if product_details['default_fee'] != 0:
                    days_difference = days_left - default_start
                    default_fee_percentage = product_details['default_fee']
                    total_default_fee = days_difference * (default_fee_percentage * emi / 100)
                elif product_details['default_fee_amount'] != 0:
                    days_difference = days_left - default_start
                    total_default_fee = days_difference * product_details['default_fee_amount']
                
                # Include lapsed fee during default period
                if days_left > lapsed_end:
                    lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                    days_in_lapsed = lapsed_end - lapsed_start
                    total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                    total_default_fee += total_lapsed_amount
                
                total_emi += total_default_fee
                self.default.text = "{:.2f}".format(total_default_fee)
                self.default.visible = True
                self.label_9.visible = True
                self.lapsed.visible = False
                self.label_5.visible = False
        
        if npa_settings:
            npa_start = int(npa_settings['minimum_days'])
            npa_end = int(npa_settings['maximum_days'])
            if npa_start < days_left <= npa_end:
                product_details = app_tables.fin_product_details.get(product_id=product_id)
                if product_details['npa'] != 0:
                    days_difference = days_left - npa_start
                    npa_percentage = product_details['npa']
                    total_npa_fee = days_difference * (npa_percentage * emi / 100)
                elif product_details['npa_amount'] != 0:
                    days_difference = days_left - npa_start
                    total_npa_fee = days_difference * product_details['npa_amount']
                
                # Include lapsed and default fees during NPA period
                if days_left > lapsed_end:
                    lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                    days_in_lapsed = lapsed_end - lapsed_start
                    total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                    total_npa_fee += total_lapsed_amount
                
                if days_left > default_end:
                    default_fee_amount = 0
                    product_details = app_tables.fin_product_details.get(product_id=product_id)
                    if product_details['default_fee'] != 0:
                        days_in_default = default_end - default_start
                        default_fee_percentage = product_details['default_fee']
                        default_fee_amount = days_in_default * (default_fee_percentage * emi / 100)
                    elif product_details['default_fee_amount'] != 0:
                        days_in_default = days_left - default_start
                        default_fee_amount = days_in_default * product_details['default_fee_amount']
                    total_npa_fee += default_fee_amount
        
                total_emi += total_npa_fee
                self.npa.text = "{:.2f}".format(total_npa_fee)
                self.npa.visible = True
                self.label_12.visible = True
                self.default.visible = False
                self.label_9.visible = False
                self.lapsed.visible = False
                self.label_5.visible = False
                
    #     if loan_state_status == 'default loan' and selected_row['days_left'] > 16:
    #       product_id = selected_row['product_id']
    # # Fetch default fee details from product details table
    #       product_details = app_tables.fin_product_details.get(product_id=product_id)
          
    #       # Check if default_fee or default_fee_amount should be used
    #       if product_details['default_fee'] != 0:
    #           # Calculate the number of days between today's date and the selected schedule payment date
    #           days_left = selected_row['days_left']
    #           days_difference = days_left - 16
      
    #           # Fetch default fee percentage and amount from product details table
    #           default_fee_percentage = product_details['default_fee']
    #           default_fee_decimal = default_fee_percentage * emi / 100
      
    #           # Calculate total default fee
    #           total_default_fee = days_difference * default_fee_decimal
      
    #       elif product_details['default_fee_amount'] != 0:
    #           # Fetch default fee amount from product details table
    #           default_fee_amount = product_details['default_fee_amount']
      
    #           # Calculate the number of days between today's date and the selected schedule payment date
    #           days_left = selected_row['days_left']
    #           days_difference = days_left - 16
      
    #           # Multiply default fee amount by days_difference
    #           total_default_fee = days_difference * default_fee_amount
      
    #       else:
    #           # Neither default_fee nor default_fee_amount is set, so default fee is zero
    #           total_default_fee = 0
      
    #       # Add default fee to total EMI
    #       total_emi += total_default_fee
    #       self.default.text = "{:.2f}".format(total_default_fee)
    #       self.default.visible = True
    #       self.label_9.visible = True
    #       self.lapsed.visible = False
    #       self.label_5.visible = False

    #     if loan_state_status == 'NPA' and selected_row['days_left'] > 106:
    # # Fetch NPA fee details from product details table
    #       product_id = selected_row['product_id']
    #       product_details = app_tables.fin_product_details.get(product_id=product_id)
          
    #       # Check if npa or npa_amount should be used
    #       if product_details['npa'] != 0:
    #           # Calculate the number of days between today's date and the selected schedule payment date
    #           days_left = selected_row['days_left']
    #           days_difference = days_left - 106
      
    #           # Fetch NPA fee percentage and amount from product details table
    #           npa_percentage = product_details['npa']
    #           npa_decimal = npa_percentage * emi/ 100
      
    #           # Calculate total NPA fee
    #           total_npa_fee = days_difference * npa_decimal
      
    #       elif product_details['npa_amount'] != 0:
    #           # Fetch NPA fee amount from product details table
    #           npa_amount = product_details['npa_amount']
      
    #           # Calculate the number of days between today's date and the selected schedule payment date
    #           days_left = selected_row['days_left']
    #           days_difference = days_left - 106
      
    #           # Multiply NPA fee amount by days_difference
    #           total_npa_fee = days_difference * npa_amount
      
    #       else:
    #           # Neither npa nor npa_amount is set, so NPA fee is zero
    #           total_npa_fee = 0
      
    #       # Add NPA fee to total EMI
    #       total_emi += total_npa_fee
      
    #       # Update UI
    #       self.npa.text = "{:.2f}".format(total_npa_fee)
    #       self.npa.visible = True
    #       self.label_12.visible = True
    #       # Hide default and lapsed fee labels
    #       self.default.visible = False
    #       self.label_9.visible = False
    #       self.lapsed.visible = False
    #       self.label_5.visible = False


        # Display the calculated EMI amount in the EMI amount label
        self.emi_amount_label.text = "{:.2f}".format(emi)  # Show only the EMI amount without extension
        
        self.update_total_emi_amount(total_emi)
        self.total_emi_amount_label.visible = True

        # Update labels based on the presence of extension amount
        if extension_amount > 0:
            self.total_emi_amount_label.text = "{:.2f}".format(total_emi)
            self.extension_amount_label.text = "{:.2f}".format(extension_amount)
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = True
            self.label_6.visible = True
            self.label_3.visible = True
        else:
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = False
            self.label_6.visible = False
            self.label_3.visible = True
  
        # Update other labels
        self.loan_id_label.text = str(selected_row['lender_full_name'])
        self.loan_amount_label.text = str(loan_amount)
        self.interest_label.text = "{:.2f}".format(total_interest_amount)
        self.tenure_label.text = str(tenure)
        self.account_no_label.text = str(selected_row['account_number'])
      
        # Display total EMI amount including extension amount
        self.update_total_emi_amount(total_emi)
      
        # foreclosure_details = self.get_foreclosure_details(loan_id, selected_row['emi_number'])
        # if foreclosure_details is not None:
        #   total_due_amount = foreclosure_details['total_due_amount']
        #   foreclosure_amount = foreclosure_details['foreclose_amount']
      
        #   lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        #   default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        #   npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
          
        #   days_left = self.selected_row['days_left']
        #   product_id = self.selected_row['product_id']
        #   # emi = self.loan_details['emi']
      
        #   if lapsed_settings:
        #       lapsed_start = lapsed_settings['minimum_days']
        #       lapsed_end = lapsed_settings['maximum_days']
        #       if lapsed_start < days_left <= lapsed_end:
        #           lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
        #           days_difference = days_left - lapsed_start
        #           total_lapsed_amount = days_difference * (lapsed_fee_percentage * emi / 100)
        #           total_due_amount += total_lapsed_amount
        #           print(f"Lapsed Fee: {total_lapsed_amount}")
      
        #   if default_settings:
        #       default_start = default_settings['minimum_days']
        #       default_end = default_settings['maximum_days']
        #       if default_start < days_left <= default_end:
        #           default_fee_amount = 0
      
        #           # Include lapsed end fee if applicable
        #           if lapsed_settings and days_left > lapsed_end:
        #               days_in_lapsed = lapsed_end - lapsed_start
        #               lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
        #               total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
        #               default_fee_amount += total_lapsed_amount
      
        #           product_details = app_tables.fin_product_details.get(product_id=product_id)
        #           if product_details['default_fee'] != 0:
        #               days_in_default = days_left - default_start
        #               default_fee_percentage = product_details['default_fee']
        #               default_fee_amount += days_in_default * (default_fee_percentage * emi / 100)
        #           elif product_details['default_fee_amount'] != 0:
        #               days_in_default = days_left - default_start
        #               default_fee_amount += days_in_default * product_details['default_fee_amount']
                  
        #           total_due_amount += default_fee_amount
        #           print(f"Default Fee: {default_fee_amount}")
      
        #   if npa_settings:
        #       npa_start = npa_settings['minimum_days']
        #       npa_end = npa_settings['maximum_days']
        #       if npa_start < days_left <= npa_end:
        #           npa_fee_amount = 0
      
        #           # Include lapsed end fee if applicable
        #           if lapsed_settings and days_left > lapsed_end:
        #               days_in_lapsed = lapsed_end - lapsed_start
        #               lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
        #               total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
        #               npa_fee_amount += total_lapsed_amount
      
        #           # Include default end fee if applicable
        #           if default_settings and days_left > default_end:
        #               days_in_default = default_end - default_start
        #               product_details = app_tables.fin_product_details.get(product_id=product_id)
        #               if product_details['default_fee'] != 0:
        #                   default_fee_percentage = product_details['default_fee']
        #                   default_fee_amount = days_in_default * (default_fee_percentage * emi / 100)
        #                   npa_fee_amount += default_fee_amount
        #               elif product_details['default_fee_amount'] != 0:
        #                   default_fee_amount = product_details['default_fee_amount']
        #                   days_in_default = days_left - default_start
        #                   default_fee_amount = days_in_default * default_fee_amount
        #                   npa_fee_amount += default_fee_amount
      
        #           product_details = app_tables.fin_product_details.get(product_id=product_id)
        #           if product_details['npa'] != 0:
        #               days_difference = days_left - npa_start
        #               npa_percentage = product_details['npa']
        #               npa_fee_amount += days_difference * (npa_percentage * emi / 100)
        #           elif product_details['npa_amount'] != 0:
        #               npa_amount = product_details['npa_amount']
        #               days_difference = days_left - npa_start
        #               npa_fee_amount += days_difference * npa_amount
                  
        #           total_due_amount += npa_fee_amount
        #           print(f"NPA Fee: {npa_fee_amount}")
      
        #   adding_remaining_part_payment = app_tables.fin_emi_table.get(
        #       loan_id=loan_id,
        #       emi_number=selected_row['emi_number']
        #   )
        #   if adding_remaining_part_payment:
        #       part_pay = adding_remaining_part_payment['payment_type']
        #       if part_pay == 'part payment':
        #           remaining_part_payment = adding_remaining_part_payment['part_payment_amount']
        #           additional_fees = self.calculate_additional_fees(adding_remaining_part_payment)
        #           print(additional_fees)
        #           self.label_14.text = additional_fees + remaining_part_payment
        #           total_due_amount += remaining_part_payment
        #           total_due_amount += additional_fees
        #           self.part_payment.enabled = False
        #           self.label_14.visible = True
        #           self.label_15.visible = True
      
        #   self.emi_amount_label.text = "{:.2f}".format(total_due_amount)
        #   self.extension_amount_label.text = "{:.2f}".format(foreclosure_amount)
        #   self.total_emi_amount_label.text = "{:.2f}".format(total_due_amount + foreclosure_amount)
        #   self.total_emi_amount_label.visible = True
        #   self.label_3.visible = True

        emi_row = app_tables.fin_emi_table.get(
            loan_id=loan_id,
            emi_number=selected_row['emi_number'] + 1
        )

        if emi_row is not None and emi_row['payment_type'] == 'part payment':
          self.button_1_copy_3.visible = False


        adding_remaining_part_payment = app_tables.fin_emi_table.get(
            loan_id=loan_id,
            emi_number=selected_row['emi_number']
        )
        if adding_remaining_part_payment:
          part_pay = adding_remaining_part_payment['payment_type']
          part_lender_returns = adding_remaining_part_payment['part_lender_returns']
          part_remaining_amount = adding_remaining_part_payment['part_remaining_amount']
          if part_pay == 'part payment':
            
            remaining_part_payment = adding_remaining_part_payment['part_payment_amount']
            # total_due_amount += remaining_part_payment
            additional_fees = self.calculate_additional_fees(adding_remaining_part_payment)
            print(additional_fees)
            self.label_14.text = additional_fees + remaining_part_payment
            # total_due_amount +=additional_fees

            total_emi += remaining_part_payment
            total_emi +=additional_fees
            self.part_payment.enabled = False
            self.label_14.visible = True
            self.label_15.visible = True 

            self.i_r.text = part_lender_returns + float(self.i_r.text)
            self.emi_processing_extension.text = part_remaining_amount + float(self.emi_processing_extension.text)
            print(self.emi_processing_extension.text)
            print(self.i_r.text)
        self.update_total_emi_amount(total_emi)


        foreclosure_details = self.get_foreclosure_details(loan_id, selected_row['emi_number'])
        if foreclosure_details is not None:
          total_due_amount = foreclosure_details['total_due_amount']
          foreclosure_amount = foreclosure_details['foreclose_amount']
          foreclosure_emi_amount = foreclosure_details['total_due_amount']
      
          lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
          default_settings = app_tables.fin_loan_settings.get(loans="default fee")
          npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
          
          days_left = self.selected_row['days_left']
          product_id = self.selected_row['product_id']
          # emi = self.loan_details['emi']
      
          if lapsed_settings:
              lapsed_start = lapsed_settings['minimum_days']
              lapsed_end = lapsed_settings['maximum_days']
              if lapsed_start < days_left <= lapsed_end:
                  lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                  days_difference = days_left - lapsed_start
                  total_lapsed_amount = days_difference * (lapsed_fee_percentage * total_due_amount / 100)
                  total_due_amount += total_lapsed_amount
                  print(f"Lapsed Fee: {total_lapsed_amount}")
                  self.lapsed.visible = True
                  self.label_5.visible = True
      
          if default_settings:
              default_start = default_settings['minimum_days']
              default_end = default_settings['maximum_days']
              if default_start < days_left <= default_end:
                  default_fee_amount = 0
      
                  # Include lapsed end fee if applicable
                  if lapsed_settings and days_left > lapsed_end:
                      days_in_lapsed = lapsed_end - lapsed_start
                      lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                      total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * total_due_amount / 100)
                      default_fee_amount += total_lapsed_amount
      
                  product_details = app_tables.fin_product_details.get(product_id=product_id)
                  if product_details['default_fee'] != 0:
                      days_in_default = days_left - default_start
                      default_fee_percentage = product_details['default_fee']
                      default_fee_amount += days_in_default * (default_fee_percentage * total_due_amount / 100)
                  elif product_details['default_fee_amount'] != 0:
                      days_in_default = days_left - default_start
                      default_fee_amount += days_in_default * product_details['default_fee_amount']
                  
                  total_due_amount += default_fee_amount
                  print(f"Default Fee: {default_fee_amount}")
                  self.default.visible = True
                  self.label_9.visible = True
      
          if npa_settings:
              npa_start = npa_settings['minimum_days']
              npa_end = npa_settings['maximum_days']
              if npa_start < days_left <= npa_end:
                  npa_fee_amount = 0
      
                  # Include lapsed end fee if applicable
                  if lapsed_settings and days_left > lapsed_end:
                      days_in_lapsed = lapsed_end - lapsed_start
                      lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                      total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * total_due_amount / 100)
                      npa_fee_amount += total_lapsed_amount
      
                  # Include default end fee if applicable
                  if default_settings and days_left > default_end:
                      days_in_default = default_end - default_start
                      product_details = app_tables.fin_product_details.get(product_id=product_id)
                      if product_details['default_fee'] != 0:
                          default_fee_percentage = product_details['default_fee']
                          default_fee_amount = days_in_default * (default_fee_percentage * total_due_amount / 100)
                          npa_fee_amount += default_fee_amount
                      elif product_details['default_fee_amount'] != 0:
                          default_fee_amount = product_details['default_fee_amount']
                          days_in_default = days_left - default_start
                          default_fee_amount = days_in_default * default_fee_amount
                          npa_fee_amount += default_fee_amount
      
                  product_details = app_tables.fin_product_details.get(product_id=product_id)
                  if product_details['npa'] != 0:
                      days_difference = days_left - npa_start
                      npa_percentage = product_details['npa']
                      npa_fee_amount += days_difference * (npa_percentage * total_due_amount / 100)
                  elif product_details['npa_amount'] != 0:
                      npa_amount = product_details['npa_amount']
                      days_difference = days_left - npa_start
                      npa_fee_amount += days_difference * npa_amount
                  
                  total_due_amount += npa_fee_amount
                  print(f"NPA Fee: {npa_fee_amount}")
                  self.npa.visible = True
                  self.label_12.visible = True
                  
      
          adding_remaining_part_payment = app_tables.fin_emi_table.get(
              loan_id=loan_id,
              emi_number=selected_row['emi_number']
          )
          if adding_remaining_part_payment:
              part_pay = adding_remaining_part_payment['payment_type']
              if part_pay == 'part payment':
                  remaining_part_payment = adding_remaining_part_payment['part_payment_amount']
                  additional_fees = self.calculate_additional_fees(adding_remaining_part_payment)
                  print(additional_fees)
                  self.label_14.text = additional_fees + remaining_part_payment
                  total_due_amount += remaining_part_payment
                  total_due_amount += additional_fees
                  self.part_payment.enabled = False
                  self.label_14.visible = True
                  self.label_15.visible = True
      
          self.emi_amount_label.text = "{:.2f}".format(foreclosure_emi_amount)
          self.extension_amount_label.text = "{:.2f}".format(foreclosure_amount)
          self.total_emi_amount_label.text = "{:.2f}".format(total_due_amount)
          self.total_emi_amount_label.visible = True
          self.label_3.visible = True

    def calculate_date_difference(self,date_to_subtract, today_date):
      return (today_date - date_to_subtract).days
      print ((today_date - date_to_subtract).days)

    def calculate_additional_fees(self, adding_remaining_part_payment):
        # Retrieve the part_payment_date from emi_row
        part_payment_date = adding_remaining_part_payment['scheduled_payment']
        print(part_payment_date)
    
        # Calculate the difference in days between part_payment_date and today's date
        days_elapsed = self.calculate_date_difference(part_payment_date, datetime.now().date())
        print(days_elapsed)
        product_id = self.selected_row['product_id']
    
        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        # Fetch necessary fee details based on loan state status and product ID
        product_details = app_tables.fin_product_details.get(product_id=product_id)
    
        # Initialize total additional fees
        total_additional_fees = 0
    
        # Check lapsed settings and calculate fees if applicable
        if lapsed_settings:
            lapsed_start = lapsed_settings['minimum_days']
            lapsed_end = lapsed_settings['maximum_days']
            if lapsed_start < days_elapsed <= lapsed_end:
                days_in_lapsed = days_elapsed - lapsed_start
                lapsed_fee_percentage = product_details['lapsed_fee']
                lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                total_additional_fees += lapsed_fee_amount
                print(f"Lapsed Fee: {lapsed_fee_amount}")
    
        # Check default settings and calculate fees if applicable
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
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                    default_fee_amount += lapsed_fee_amount
    
                if product_details['default_fee'] != 0:
                    default_fee_percentage = product_details['default_fee']
                    default_fee_amount += days_in_default * (default_fee_percentage * float(self.emi.text) / 100)
                elif product_details['default_fee_amount'] != 0:
                    default_fee_amount += days_in_default * product_details['default_fee_amount']
                
                total_additional_fees += default_fee_amount
                print(f"Default Fee: {default_fee_amount}")
    
        # Check NPA settings and calculate fees if applicable
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
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                    npa_fee_amount += lapsed_fee_amount
    
                # Include default end fee if applicable
                if default_settings and days_elapsed > default_end:
                    days_in_default = default_end - default_start
                    if product_details['default_fee'] != 0:
                        default_fee_percentage = product_details['default_fee']
                        default_fee_amount = days_in_default * (default_fee_percentage * float(self.emi.text) / 100)
                        npa_fee_amount += default_fee_amount
                    elif product_details['default_fee_amount'] != 0:
                        default_fee_amount = days_in_default * product_details['default_fee_amount']
                        npa_fee_amount += default_fee_amount
    
                if product_details['npa'] != 0:
                    npa_fee_percentage = product_details['npa']
                    npa_fee_amount += days_in_npa * (npa_fee_percentage * float(self.emi.text) / 100)
                elif product_details['npa_amount'] != 0:
                    npa_fee_amount += days_in_npa * product_details['npa_amount']
                
                total_additional_fees += npa_fee_amount
                print(f"NPA Fee: {npa_fee_amount}")
    
        print(f"Total Additional Fees: {total_additional_fees}")
        return total_additional_fees
  
          
  
    def get_extension_details(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=self.selected_row['borrower_customer_id'],
            loan_id=loan_id,
            emi_number=q.less_than_or_equal_to(emi_number)
        )
        extension_months = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_months = extension_row['total_extension_months']
        return  extension_months

    def get_extension_details_1(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=self.selected_row['borrower_customer_id'],
            loan_id=loan_id,
            emi_number=emi_number
        )
        extension_amount = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_amount = extension_row['extension_amount']
        return extension_amount

    def get_foreclosure_details(self, loan_id, emi_number):
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number,
      )
      
      if foreclosure_row is not None and foreclosure_row['status'] == 'approved':
          return foreclosure_row
      else:
          return None
  
    def update_total_emi_amount(self, total_emi):
        self.total_emi_amount_label.text = "{:.2f}".format(total_emi)

    def get_first_payment_due_date(self, loan_id):
        loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
        if loan_row is not None:
            return loan_row['first_emi_payment_due_date']
        else:
            return None  # or handle the case where the loan ID is not found

    def pay_now_click(self, **event_args):
        remaining_tenure = self.remaining_tenure.text
        i_r = float(self.i_r.text)
        print('lender return')
        print(i_r)

        emi_amount_for_remaining_amount = float(self.emi_processing_extension.text)
        total_emi_amount = float(self.total_emi_amount_label.text)
        # Calculate total EMI amount including processing fees
        emi_amount = float(self.emi_amount_label.text)
        # Retrieve total repayment amount from loan details table
        total_repayment_amount = self.selected_row['total_repayment_amount']
        # Retrieve processing fee
        processing_fee = float(self.processing_fee.text)  # Assuming processing fee is shown in label_9
 
        try:
            lapsed_fee = float(self.lapsed.text)
        except ValueError:
            lapsed_fee = 0.0  # Default value if conversion fails
        
        try:
            default_fee = float(self.default.text)
        except ValueError:
            default_fee = 0.0

        try:
            extra_amount = float(self.extension_amount_label.text)
        except ValueError:
            extra_amount = 0.0

       # extra_amount = float(self.extension_amount_label.text)
        try:
            npa = float(self.npa.text)
        except ValueError:
            npa = 0.0

       # extra_amount = float(self.extension_amount_label.text)
        extra_fee = lapsed_fee + default_fee + extra_amount + npa
        total_extra_fee = lapsed_fee + default_fee + extra_amount + processing_fee + npa
      
        # total_emi_amount = float(self.total_emi_amount_label.text)  # Fetch total EMI amount including extra payment
        borrower_wallet = app_tables.fin_wallet.get(customer_id=self.user_id)
        print(self.selected_row['lender_customer_id'])
        print(self.selected_row['borrower_customer_id'])
        # transfer_money(lender_id = self.selected_row['lender_customer_id'], borrower_id=self.selected_row['borrower_customer_id'], transfer_amount=total_emi_amount) 

        if borrower_wallet is not None:
            wallet_balance = borrower_wallet['wallet_amount']

            if wallet_balance >= total_emi_amount:
                updated_balance = wallet_balance - total_emi_amount
                borrower_wallet['wallet_amount'] = updated_balance
                borrower_wallet.update()

                # Retrieve lender's wallet based on lender_customer_id
                lender_wallet = app_tables.fin_wallet.get(customer_id=self.selected_row['lender_customer_id'])
                transfer_money_1(lender_id = self.selected_row['lender_customer_id'], borrower_id=self.selected_row['borrower_customer_id'], transfer_amount=total_emi_amount) 

                if lender_wallet is not None:
                    lender_balance = lender_wallet['wallet_amount']

                    # If lender_balance is None, treat it as zero
                    if lender_balance is None:
                        lender_balance = 0

                    lender_balance += total_emi_amount  # Add deducted amount to lender's wallet
                    lender_wallet['wallet_amount'] = lender_balance
                    lender_wallet.update()


                    existing_fee_rows = app_tables.fin_platform_details.get()
                    if existing_fee_rows is None:
                      app_tables.fin_platform_details.add_row(platform_returns=total_extra_fee)
                    else:
                      existing_fee_rows['platform_returns'] +=total_extra_fee
                      existing_fee_rows.update()
                  
                    if self.selected_row['remaining_amount'] is not None:
                        remaining_amount = self.selected_row['remaining_amount'] - emi_amount_for_remaining_amount#(emi_amount + processing_fee + extra_amount)
                    else:
                        remaining_amount = total_repayment_amount - emi_amount_for_remaining_amount #(emi_amount + processing_fee + extra_amount)
            
                    print(remaining_amount)
                    loan_details = app_tables.fin_loan_details.get(loan_id=self.selected_row['loan_id'])
                    if loan_details is not None:
                        if loan_details['total_amount_paid'] is None :
                            loan_details['total_amount_paid'] = 0
                        if loan_details['lender_returns'] is None :
                            loan_details['lender_returns'] = 0
                        loan_details['lender_returns'] += round(i_r ,2)
                        if remaining_tenure == 0:
                          loan_details['remaining_amount'] -= emi_amount
                        else:
                          loan_details['remaining_amount'] = round(remaining_amount ,2)
                        loan_details['total_amount_paid'] += round(total_emi_amount ,2)
                        if loan_details['remaining_amount'] <= 0:
                          loan_details['loan_updated_status'] = 'closed'
                          
                          lender_data = app_tables.fin_lender.get(customer_id=self.selected_row['lender_customer_id'])
                          if lender_data:
                            lender_data['present_commitments'] -= self.selected_row['loan_amount']
                            lender_data.update()
                            
                        loan_details.update()
            
                    lender_returns_dict = defaultdict(float)
                    borrower_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.selected_row['borrower_customer_id'])
                    for loan in borrower_loans:
                        lender_id = loan['lender_customer_id']
                        lender_returns = loan['lender_returns']
                        # Convert None to 0 for lender returns
                        if lender_returns is None:
                            lender_returns = 0
                        lender_returns_dict[lender_id] += lender_returns
                    # Update lender returns in the fin_lender table
                    for lender_id, total_returns in lender_returns_dict.items():
                        lender_row = app_tables.fin_lender.get(customer_id=lender_id)
                        if lender_row is not None:
                            if lender_row['return_on_investment'] is None:
                                lender_row['return_on_investment'] = 0
                            lender_row['return_on_investment'] = total_returns
                            lender_row.update()
                        else:
                            # Create a new row if lender doesn't exist
                            app_tables.fin_lender.add_row(customer_id=lender_id, return_on_investment=total_returns)

                      

                    # self.update_payment_status()

                    loan_id = self.selected_row['loan_id']
                    current_emi_number = int(self.selected_row['emi_number'])
                    account_number = self.selected_row['account_number']
                    emi_payment_type = self.selected_row['emi_payment_type']
                    tenure = self.selected_row['tenure']
                    borrower_id = self.selected_row['borrower_customer_id']
                    lender_id = self.selected_row['lender_customer_id']
                    lender_email = self.selected_row['lender_email_id']
                    borrower_email = self.selected_row['borrower_email_id']
                    days_left = self.selected_row['days_left']

                    prev_scheduled_payment = self.selected_row['scheduled_payment']
                    prev_next_payment = self.selected_row['next_payment']

                  
                    # Calculate next scheduled payment based on emi_payment_type
                    if emi_payment_type in ['One Time', 'Monthly', 'Three Months', 'Six Months']:
                        
                        if emi_payment_type == 'Monthly':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                            next_next_payment = prev_next_payment + timedelta(days=30)
                        elif emi_payment_type == 'Three Months':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=90)
                            next_next_payment = prev_next_payment + timedelta(days=90)
                     
                        elif emi_payment_type == 'Six Months':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=180)
                            next_next_payment = prev_next_payment + timedelta(days=180)
                        elif emi_payment_type == 'One Time':
                          if tenure:
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30 * tenure)
                            next_next_payment = self.selected_row['next_payment'] + timedelta(days=30 * tenure)                
                    else:
                        # Default to monthly calculation
                        next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                        next_next_payment = prev_next_payment + timedelta(days=30)

                    # Add a new row to fin_emi_table
                    new_emi_row = app_tables.fin_emi_table.add_row(
                        loan_id=loan_id,
                        emi_number=current_emi_number + 1,
                        account_number=account_number,
                        scheduled_payment_made=datetime.now(),
                        scheduled_payment=next_scheduled_payment,
                        next_payment=next_next_payment,
                        amount_paid= total_emi_amount,
                        extra_fee=extra_fee,
                        borrower_customer_id=borrower_id,
                        lender_customer_id=lender_id,
                        borrower_email=borrower_email,
                        lender_email=lender_email,
                        payment_type='pay now',
                        remaining_tenure=remaining_tenure,
                        days_left=days_left,
                        npa_fee=npa,
                        default_fee=default_fee,
                        lapsed_fee=lapsed_fee,
                        total_remaining_amount= round(remaining_amount,2),
                        total_platform_fee=total_extra_fee,
                        lender_returns=round(i_r,2),
                        
                        
                    )

                    # Update the emi_number and next_payment in the selected_row
                    self.selected_row['emi_number'] = current_emi_number + 1
                    self.selected_row['next_payment'] = next_next_payment
                    self.selected_row.update()

                    foreclosure_row = self.get_foreclosure_details_for_status_rejection(self.selected_row['loan_id'], self.selected_row['emi_number'])
                    if foreclosure_row is not None and foreclosure_row['status'] == 'under process':
                        # Update status to 'rejected'
                        foreclosure_row['status'] = 'rejected'
                        foreclosure_row.update()

                  
                    if self.foreclosure_condition_satisfied(loan_id, current_emi_number):
                      self.update_loan_status(loan_id, 'close')

                    #self.status_label.text = "Payment successfully done..."
                    # self.button_1_copy_3.visible = False
                    alert('Payment successfully done...')
                    open_form('borrower.dashboard')
                else:
                    alert( "Lender's wallet not found.")
            else:
                alert("Insufficient funds in wallet. Please deposit more funds to continue.")
                open_form('wallet.wallet')
        else:
            self.status_label.text = "Wallet record not found."

    def button_1_copy_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard.today_dues')

    def update_loan_status(self, loan_id, new_status):
    # Update loan status in the loan details table for the given loan ID
      loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
      if loan_row is not None:
          loan_row['loan_updated_status'] = new_status
          loan_row.update()


    def foreclosure_condition_satisfied(self, loan_id, emi_number):
    # Check if foreclosure details are returned for the given loan and EMIs
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number,
        
      )
      if foreclosure_row is not None and foreclosure_row['status'] == 'approved':
          return foreclosure_row
      else:
          return None

    # def update_payment_status(self):
    # # Update payment status in loan details table for the given loan ID, borrower ID, and condition
    #   loan_details = app_tables.fin_loan_details.search(
    #     loan_id=self.selected_row['loan_id'],
    #     borrower_customer_id=self.selected_row['borrower_customer_id'],
    #     first_emi_payment_due_date=q.less_than_or_equal_to(datetime.now().date())
    # )
    #   for loan_detail in loan_details:
    #     loan_detail['payment_status'] = True
    #     loan_detail.update()


    def get_foreclosure_details_for_status_rejection(self, loan_id, emi_number):
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number - 1,
      )
      
      if foreclosure_row is not None :
          return foreclosure_row
      else:
          return None

    def part_payment_click(self, **event_args):
      """This method is called when the button is clicked"""

      try:
        # Try to convert and get the values, and calculate the extra fee
        lapsed_fee = float(self.lapsed.text)
      except ValueError:
          lapsed_fee = 0.0
          
      try:
          default_fee = float(self.default.text)
      except ValueError:
          default_fee = 0.0
          
      try:
          extension_amount = float(self.extension_amount_label.text)
      except ValueError:
          extension_amount = 0.0
          
      try:
          npa_fee = float(self.npa.text)
      except ValueError:
          npa_fee = 0.0

      processing_fee = float(self.processing_fee.text)
      # Calculate the extra fee
      extra_fee = lapsed_fee + default_fee + extension_amount + npa_fee
      total_extra_fee = lapsed_fee + default_fee + extension_amount + processing_fee
      loan_details = {
        'i_r': self.i_r.text,
        'emi': self.emi.text,
        'total_emi_amount': self.total_emi_amount_label.text,
        'emi_amount': self.emi_amount_label.text,
        'loan_id': self.selected_row['loan_id'],
        'loan_amount': self.loan_amount_label.text,
        'tenure': self.tenure_label.text,
        'account_no': self.account_no_label.text,
        'interest_amount': self.interest_label.text,
        'remainining_amount': self.remainining_amount.text,
        'borrower_customer_id': self.selected_row['borrower_customer_id'],
        'lender_customer_id': self.selected_row['lender_customer_id'],
        'lender_email' : self.selected_row['lender_email_id'],
        'borrower_email' : self.selected_row['borrower_email_id'],
        'emi_payment_type' : self.selected_row['emi_payment_type'],
        'current_emi_number' : int(self.selected_row['emi_number']),
        'extra_fee':extra_fee,
        'total_extra_fee':total_extra_fee,
        'prev_scheduled_payment' : self.selected_row['scheduled_payment'],
        'prev_next_payment' : self.selected_row['next_payment'],
        'product_id' : self.selected_row['product_id'],
        'loan_state_status' : self.selected_row['loan_state_status'],
        # 'part_payment_date' : self.selected_row['part_payment_date'],
        # 'payment_type' : self.selected_row['payment_type'],
        # 'tenure':self.tenure_label.text,
        'lender_full_name' : self.selected_row['lender_full_name'],
        'for_remaining_amount_calculation': self.emi_processing_extension.text,
        # 'remaining_tenure': self.tenure_label.text,
        'remaining_tenure' : self.selected_row['remaining_tenure'],
        'days_left' : self.selected_row['days_left'],
        'npa_fee':npa_fee,
        'default_fee':default_fee,
        'lapsed_fee':lapsed_fee,
    }
    
    # Open the part_payment form and pass loan_details as a parameter
      open_form('borrower.dashboard.today_dues.check_out.part_payment', loan_details=loan_details, selected_row=self.selected_row)

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('borrower.dashboard.today_dues')
