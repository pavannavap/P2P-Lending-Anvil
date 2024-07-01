from ._anvil_designer import today_duesTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone, timedelta
from .. import main_form_module as main_form_module

class today_dues(today_duesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.user_id = main_form_module.userId
        self.init_components(**properties)
        
        today_date = datetime.now(timezone.utc).date()
        loan_details = []

        all_loans_disbursed = app_tables.fin_loan_details.search(
            loan_updated_status=q.any_of("disbursed", "extension", "foreclosure"),
            first_emi_payment_due_date=q.less_than_or_equal_to(today_date),
            borrower_customer_id=self.user_id
        )
    
        for loan in all_loans_disbursed:
            loan_id = loan['loan_id']
            borrower_customer_id = loan['borrower_customer_id']

            payment_done = list(app_tables.fin_emi_table.search(
                loan_id=loan_id,
                next_payment=q.greater_than(today_date),
                payment_type ='pay now',
                borrower_customer_id=borrower_customer_id
            ))
            if payment_done:
              payment_done.sort(key=lambda x: x['next_payment'], reverse=True)
              latest_payment_done = payment_done[0]
              if latest_payment_done:
                continue
              
            all_loans = list(app_tables.fin_emi_table.search(
                loan_id=loan_id,
                next_payment=q.less_than_or_equal_to(today_date),
                borrower_customer_id=borrower_customer_id
            ))
            
            if all_loans:
                all_loans.sort(key=lambda x: x['next_payment'], reverse=True)
                latest_loan = all_loans[0]
                loan_detail = app_tables.fin_loan_details.get(loan_id=latest_loan['loan_id'])
                user_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['lender_customer_id'])
                if loan_detail is not None and user_profile is not None  and (loan_detail['remaining_amount'] is  None or loan_detail['remaining_amount'] > 0):        
                    loan_amount = loan_detail['loan_amount']
                    scheduled_payment = latest_loan['scheduled_payment']
                    next_payment = latest_loan['next_payment']
                    days_left = (today_date - next_payment).days
               
                    emi_number = latest_loan['emi_number']
                    account_number = latest_loan['account_number']
                    tenure = loan_detail['tenure']
                    interest_rate = loan_detail['interest_rate']
                    borrower_loan_created_timestamp = loan_detail['borrower_loan_created_timestamp']
                    loan_updated_status = loan_detail['loan_updated_status']
                    loan_disbursed_timestamp = loan_detail['loan_disbursed_timestamp']
                    emi_payment_type = loan_detail['emi_payment_type']
                    lender_customer_id = loan_detail['lender_customer_id']
                    borrower_customer_id = loan_detail['borrower_customer_id']
                    first_emi_payment_due_date = loan_detail['first_emi_payment_due_date']
                    total_repayment_amount = loan_detail['total_repayment_amount']
                    total_processing_fee_amount = loan_detail['total_processing_fee_amount']
                    mobile = user_profile['mobile']
                    user_photo = user_profile['user_photo']
                    product_name = loan_detail['product_name']
                    product_description = loan_detail['product_description']
                    lender_full_name = loan_detail['lender_full_name']
                    loan_state_status = loan_detail['loan_state_status']
                    product_id = loan_detail['product_id']
                    total_interest_amount = loan_detail['total_interest_amount']
                    Scheduled_date = latest_loan['next_payment']
                    lender_email_id = loan_detail['lender_email_id']
                    borrower_email_id = loan_detail['borrower_email_id']
                    total_amount_paid = loan_detail['total_amount_paid']
                    remaining_amount = loan_detail['remaining_amount']
                    payment_type = latest_loan['payment_type']
                    part_payment_date = latest_loan['part_payment_date']
                    remaining_tenure = latest_loan['remaining_tenure']
                  
                    loan_details.append({
                        'loan_id': loan_id,
                        'loan_amount': loan_amount,
                        'scheduled_payment': scheduled_payment,
                        'days_left': days_left,
                        'tenure': tenure,
                        'interest_rate': interest_rate,
                        'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
                        'emi_number': emi_number,
                        'account_number': account_number,
                        'loan_updated_status': loan_updated_status,
                        'loan_disbursed_timestamp': loan_disbursed_timestamp,
                        'next_payment': next_payment,
                        'emi_payment_type': emi_payment_type,
                        'lender_customer_id': lender_customer_id,
                        'first_emi_payment_due_date': first_emi_payment_due_date,
                        'total_repayment_amount': total_repayment_amount,
                        'total_processing_fee_amount': total_processing_fee_amount,
                        'mobile': mobile,
                        'product_description': product_description,
                        'product_name': product_name,
                        'lender_full_name': lender_full_name,
                        'borrower_customer_id': borrower_customer_id,
                        'loan_state_status': loan_state_status,
                        'product_id':product_id,
                        'total_interest_amount':total_interest_amount,
                        'Scheduled_date':Scheduled_date,
                        'user_photo':user_photo,
                        'lender_email_id':lender_email_id,
                        'borrower_email_id':borrower_email_id,
                        'total_amount_paid':total_amount_paid,
                        'remaining_amount':remaining_amount,
                        'payment_type': payment_type,
                        'part_payment_date':part_payment_date,
                        'remaining_tenure':remaining_tenure,
                    })
            else:
                pay_now_loan = app_tables.fin_emi_table.search(
                    loan_id=loan_id,
                    payment_type="pay now"
                )
                if any(pay_now_loan):
                    continue

                loan_detail = app_tables.fin_loan_details.get(loan_id=loan_id)

                  
                user_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['lender_customer_id'])

                if loan_detail is not None and user_profile is not None and (loan_detail['remaining_amount'] is  None or loan_detail['remaining_amount'] > 0):
                  user_photo = user_profile['user_photo']
                  loan_amount = loan_detail['loan_amount']
                  first_emi_payment_due_date = loan_detail['first_emi_payment_due_date']
                  days_left = (today_date - first_emi_payment_due_date).days
                  # Fetch account number from user profile table based on customer_id
                  user_profile_1 = app_tables.fin_user_profile.get(customer_id=loan_detail['borrower_customer_id'])
                  if user_profile_1 is not None:
                      account_number = user_profile['account_number']
                  else:
                      account_number = "N/A"
                  
                  # Set emi_number to 0
                
                    
                  
                  emi_number = 0
                  remaining_tenure = 0
                  tenure = loan_detail['tenure']
                  interest_rate = loan_detail['interest_rate']
                  borrower_loan_created_timestamp = loan_detail['borrower_loan_created_timestamp']
                  loan_updated_status = loan_detail['loan_updated_status']
                  loan_disbursed_timestamp = loan_detail['loan_disbursed_timestamp']
                  emi_payment_type = loan_detail['emi_payment_type']
                  lender_customer_id = loan_detail['lender_customer_id']
                  total_repayment_amount = loan_detail['total_repayment_amount']
                  total_processing_fee_amount = loan_detail['total_processing_fee_amount']
                  mobile = user_profile['mobile']
                  product_name = loan_detail['product_name']
                  product_description = loan_detail['product_description']
                  borrower_customer_id = loan_detail['borrower_customer_id']
                  lender_full_name = loan_detail['lender_full_name']
                  scheduled_payment = loan_disbursed_timestamp.date()
                  loan_state_status = loan_detail['loan_state_status']
                  product_id =loan_detail['product_id']
                  total_interest_amount  = loan_detail['total_interest_amount']
                  Scheduled_date = loan_detail['first_emi_payment_due_date']
                  lender_email_id = loan_detail['lender_email_id']
                  borrower_email_id = loan_detail['borrower_email_id']
                  total_amount_paid = loan_detail['total_amount_paid']
                  remaining_amount = loan_detail['remaining_amount']

                  
                  # Calculate next_payment based on first_payment_due_date
                  if emi_payment_type == 'One Time':
                      if tenure:
                          next_payment = loan_disbursed_timestamp.date() + timedelta(days=30 * tenure)
                  elif emi_payment_type == 'Monthly':
                      # For monthly payment, set next_payment to a month after first_payment_due_date
                      next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
                  elif emi_payment_type == 'Three Months':
                      # For three-month payment, set next_payment to three months after first_payment_due_date
                      next_payment = loan_disbursed_timestamp.date() + timedelta(days=90)
                  elif emi_payment_type == 'Six Months':
                      # For six-month payment, set next_payment  six months after first_payment_due_date
                      next_payment = loan_disbursed_timestamp.date() + timedelta(days=180)
                  else:
                      # Default to monthly calculation if emi_payment_type is not recognized
                      next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
                  
                  loan_details.append({
                      'loan_id': loan_id,
                      'loan_amount': loan_amount,
                      'scheduled_payment': scheduled_payment,   # Set scheduled_payment to first_payment_due_date first_emi_payment_due_date
                      'next_payment': next_payment,
                      'days_left': days_left,
                      'tenure': tenure,
                      'interest_rate': interest_rate,
                      'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
                      'loan_updated_status': loan_updated_status,
                      'loan_disbursed_timestamp': loan_disbursed_timestamp,
                      'emi_number': emi_number,
                      'account_number': account_number,
                      'emi_payment_type': emi_payment_type,
                      'lender_customer_id': lender_customer_id,
                      'total_repayment_amount': total_repayment_amount,
                      # 'first_payment_due_date': first_payment_due_date
                      'total_processing_fee_amount': total_processing_fee_amount,
                      'mobile': mobile,
                      'product_description': product_description,
                      'product_name': product_name,
                      'lender_full_name': lender_full_name,  
                      'borrower_customer_id': borrower_customer_id,
                      'loan_state_status':loan_state_status,
                      'product_id':product_id,
                      'total_interest_amount':total_interest_amount,
                      'Scheduled_date':Scheduled_date,
                      'user_photo' : user_photo,
                      'lender_email_id':lender_email_id,
                      'borrower_email_id':borrower_email_id,
                      'total_amount_paid':total_amount_paid,
                      'remaining_amount':remaining_amount,
                      'remaining_tenure':remaining_tenure
                      
                  })
            self.repeating_panel_2.items = loan_details
            # for loan_detail_1 in loan_details:
            #   print("Processing loan:", loan_detail_1)
            #   if loan_detail_1['days_left'] > 6 and loan_detail_1['days_left'] <= 16:
            #       print("Updating status to 'lapsed loan'")
            #       loan_detail_1['loan_state_status'] = 'lapsed loan'
            #       loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail_1['loan_id'])
            #       if loan_row is not None:
            #           loan_row['loan_state_status'] = 'lapsed loan'
            #           loan_row.update()
            #   elif loan_detail_1['days_left'] > 16 and loan_detail_1['days_left'] <= 106:
            #       print("Updating status to 'default loan'")
            #       loan_detail_1['loan_state_status'] = 'default loan'
            #       loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail_1['loan_id'])
            #       if loan_row is not None:
            #           loan_row['loan_state_status'] = 'default loan'
            #           loan_row.update()
            #   elif loan_detail_1['days_left'] > 106:
            #       print("Updating status to 'default loan'")
            #       loan_detail_1['loan_state_status'] = 'NPA'
            #       loan_row = app_tables.fin_loan_details.get(loan_id=loan_detail_1['loan_id'])
            #       if loan_row is not None:
            #           loan_row['loan_state_status'] = 'NPA'
            #           loan_row.update()

    def home_borrower_registration_form_copy_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.dashboard')

