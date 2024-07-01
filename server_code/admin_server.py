import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *
import math
import requests
import random
from email.message import EmailMessage
import bcrypt
import anvil.pdf
from datetime import datetime, time ,timedelta



@anvil.server.callable
def check_user_profile(email):
    return app_tables.users.get(email=email)

@anvil.server.callable
def send_email_otp(email):
    otp = random.randint(100000, 999999)

    from_email = "gtpltechnologies@gmail.com"  # Use your verified email address
    subject = "OTP Verification"
    content = f"Your OTP is: {otp}"

    try:
        anvil.email.send(to=email, from_address=from_email, subject=subject, text=content)
        return otp  # If successful, return OTP
    except Exception as e:
        print(f"Error sending email: {e}")
        return str(e)  # Return error message
@anvil.server.callable
def update_user_status(email, email_verified):
    user = app_tables.users.get(email=email)
    if user:
        user['email_verified'] = email_verified
    else:
        # If user does not exist, create a new row
        user = app_tables.users.add_row(email=email, email_verified=email_verified)
    return True

@anvil.server.callable
def create_receipt_pdf(name, image_source,selected_row):    
    # Your PDF creation logic here
    pdf = anvil.pdf.PDFRenderer(landscape=True).render_form("admin.dashboard.accounting.payment_receipt.emi_details.payment_receipts",selected_row = selected_row)  
    return pdf

@anvil.server.callable
def create_receipt_pdf1(name, image_source,selected_row):    
    # Your PDF creation logic here
    pdf = anvil.pdf.PDFRenderer(landscape=True).render_form("admin.dashboard.accounting.payment_receipt.emi_details")  
    return pdf
  
# Define server function to navigate to the Invest Now form
@anvil.server.callable
def open_invest_now_form():
    open_form("bank_users.main_form.basic_registration_form")

@anvil.server.callable
def open_apply_for_loan_form():
    open_form("bank_users.main_form.basic_registration_form")


@anvil.server.callable
def product_details(product_id, product_name, product_group,product_description, product_categories,processing_fee,tds,extension_fee, membership_type, interest_type, max_amount, min_amount, min_tenure, max_tenure, roi, foreclose_type, foreclosure_fee, extension_allowed, emi_payment, min_months,lapsed_fee, default_fee, default_fee_amount, npa , npa_amount, occupation,min_extension_month ,default_status, npa_status):
  row = app_tables.fin_product_details.add_row(product_id=product_id,
                                           product_name = product_name,
                                           product_group=product_group,
                                           product_description = product_description,
                                           product_categories = product_categories,
                                           processing_fee=processing_fee,
                                           tds = tds,
                                           extension_fee=extension_fee,
                                           membership_type=membership_type,
                                           interest_type= interest_type,
                                           # late_fee = late_fee,
                                           max_amount = max_amount,
                                           min_amount=min_amount,
                                           # tenure = tenure,
                                           min_tenure = min_tenure,
                                           max_tenure = max_tenure,
                                           roi = roi,
                                           foreclose_type=foreclose_type,
                                           foreclosure_fee = foreclosure_fee,
                                           extension_allowed=extension_allowed,
                                           # lapsed_status=lapsed_status,
                                           emi_payment = emi_payment,
                                           min_months=min_months,                                           
                                           #discount_coupons = discount_coupons,
                                           lapsed_fee = lapsed_fee,
                                           default_fee = default_fee,
                                           default_fee_amount = default_fee_amount,
                                           npa=npa,
                                           npa_amount=npa_amount,
                                           occupation=occupation,
                                           min_extension_months=min_extension_month,
                                           default_select_percentage_amount = default_status,
                                           npa_select_percentage_amount=npa_status
                                          )



@anvil.server.callable
def manage_products(groups,category):
  row = app_tables.fin_product_categories.add_row(product_group=groups,product_category=category)


@anvil.server.callable
def user_issues_bugreports(user_issues, specific_issue, user_discription, image, feedback_form, email_user,coustmer_id):
 row = app_tables.fin_user_issues_bugreports.add_row(user_issues=user_issues,
                                                 user_discription=user_discription,
                                                 specific_issue=specific_issue,
                                                 image=image,
                                                 feedback_form=feedback_form,
                                                 email_user=email_user,
                                                 customer_id=coustmer_id)

# code for basic details
@anvil.server.callable
def add_basic_details(full_name, gender, dob, mobile_no, user_photo, alternate_email, aadhar, aadhar_card, pan, pan_card, street_adress_1, street_address_2, city, pincode, state, country, user_id, user_age ,present, duration):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['full_name'] = full_name
    row[0]['gender'] = gender
    row[0]['date_of_birth'] = dob
    row[0]['mobile']=mobile_no
    row[0]['user_photo']=user_photo
    row[0]['another_email']= alternate_email
    row[0]['aadhaar_no']=aadhar
    row[0]['aadhaar_photo']=aadhar_card
    row[0]['pan_number']=pan
    row[0]['pan_photo']=pan_card
    row[0]['street_adress_1'] = street_adress_1
    row[0]['street_address_2'] = street_address_2
    row[0]['city'] = city
    row[0]['state'] = state
    row[0]['country'] = country
    row[0]['pincode'] = pincode
    row[0]['user_age'] = user_age
    row[0]['present_address'] = present
    row[0]['duration_at_address'] = duration
    row[0]['form_count'] = 0

@anvil.server.callable
def generate_admin_id():
    full_table = app_tables.fin_user_profile.search()
    if full_table:
        highest_customer_id = find_highest_customer_id()
        return highest_customer_id + 1
    else:
        return 100000

def find_highest_customer_id():
    table_data = app_tables.fin_user_profile.search()
    highest_id = 99999
    for row in table_data:
        customer_id = row['customer_id']
        if customer_id > highest_id:
            highest_id = customer_id
    return highest_id

@anvil.server.callable
def generate_field_engineer_id():
    full_table = app_tables.fin_user_profile.search()
    if full_table:
        highest_customer_id = find_highest_customer_id()
        return highest_customer_id + 1
    else:
        return 100000

# def find_highest_customer_id():
#     table_data = app_tables.fin_user_profile.search()
#     highest_id = 99999
#     for row in table_data:
#         customer_id = row['customer_id']
#         if customer_id > highest_id:
#             highest_id = customer_id
#     return highest_id

import bcrypt

@anvil.server.callable
def hash_password(password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()

# for view admins
@anvil.server.callable
def get_admin_emails():
    # Fetch all admin emails from the fin_admin_users table
    admin_emails = [admin['admin_email'] for admin in app_tables.fin_admin_users.search()]
    return admin_emails

@anvil.server.callable
def get_admin_details(email):
    # Fetch admin details based on email from the fin_admin_users table
    admin = app_tables.fin_admin_users.get(admin_email=email)
    if admin:
        admin_details = {
            'admin_email': admin['admin_email'],
            'full_name': admin['full_name'],
            'admin_role':admin['admin_role'],
            'ref_admin_name':admin['ref_admin_name'],
            'joined_date':admin['join_date']
        }
        return admin_details
    else:
        return None


@anvil.server.callable
def get_user_for_login(email):
  user_by_username = app_tables.users.get(email=email)

  if user_by_username:
            return user_by_username
  else:
            return None


@anvil.server.callable
def hash_password_1(password ,password_hash):
    # Hash the password using bcrypt
    hashed_password = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    return hashed_password

@anvil.server.callable
def hash_password_2(password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()

@anvil.server.callable
def search_borrower(query):
  result = app_tables.fin_user_profile.search(usertype=q.like('borrower'))
  if query:
    result = [
      x for x in result
      if query in str(x['customer_id'])
      or query in str(x['full_name'])
      or query in str(x['mobile'])
      or query in str(x['email_user'])
    ]
  return result

@anvil.server.callable
def search_lender(query):
  result = app_tables.fin_user_profile.search(usertype=q.like('lender'))
  if query:
    result = [
      x for x in result
      if query in str(x['customer_id'])
      or query in str(x['full_name'])
      or query in str(x['mobile'])
      or query in str(x['email_user'])
    ]
  return result

# # Server module: manage_credit_limit.py


@anvil.server.callable
def save_credit_limit(new_value):
    row = app_tables.fin_manage_credit_limit.get()  # Get the single row in the table
    if row:
        row['credit_limit'] = new_value  # Update the existing row
    else:
        app_tables.fin_manage_credit_limit.add_row(credit_limit=new_value)  # Add a new row if none exists

#manage_customer and contact details server code

def load_customer_data(self):
  # Fetch the customer data from the server function
  user_profile = anvil.server.call('get_customer_data')
  
  # Set the items property of the repeating panel to the fetched data
  self.repeating_panel_1.items = user_profile


@anvil.server.callable
def get_combined_user_and_guarantor_data():
    # Fetch user profiles excluding "super admin" and "admin"
    user_profiles = app_tables.fin_user_profile.search()
    
    # Fetch all guarantors
    guarantors = app_tables.fin_guarantor_details.search()

    # Create a list of customer_ids to exclude (super admin and admin)
    restricted_customer_ids = [profile['customer_id'] for profile in user_profiles if profile['usertype'] in ['super admin', 'admin']]
    
    # Filter user profiles to exclude restricted customer_ids
    user_profiles_filtered = [profile for profile in user_profiles if profile['customer_id'] not in restricted_customer_ids]
    
    # Filter guarantors to exclude restricted customer_ids
    guarantors_filtered = [guarantor for guarantor in guarantors if guarantor['customer_id'] not in restricted_customer_ids]

    # Combine the data into a single list, interleaving records
    combined_data = []

    # Determine the maximum length to iterate up to the maximum of both lists
    max_length = max(len(user_profiles_filtered), len(guarantors_filtered))

    for i in range(max_length):
        if i < len(user_profiles_filtered) and i < len(guarantors_filtered):
            user_profile = user_profiles_filtered[i]
            guarantor = guarantors_filtered[i]
            combined_data.append({
                'user_photo': user_profile['user_photo'],  
                'full_name': user_profile['full_name'],   
                'email_user': user_profile['email_user'],  
                'mobile': user_profile['mobile'],  
                'usertype': user_profile['usertype'],
                'another_person': guarantor['another_person'],  
                'guarantor_name': guarantor['guarantor_name'],   
                'guarantor_mobile_no': guarantor['guarantor_mobile_no']
            })
        

    return combined_data


@anvil.server.callable
def get_combined_user_and_guarantor_data_2():
    # Fetch user profiles
    user_profiles = app_tables.fin_user_profile.search()

    # Create a list of customer_ids to exclude (super admin and admin)
    restricted_customer_ids = [profile['customer_id'] for profile in user_profiles if profile['usertype'] in ['super admin', 'admin']]
    
    # Filter user profiles to exclude restricted customer_ids
    user_profiles_filtered = [profile for profile in user_profiles if profile['customer_id'] not in restricted_customer_ids]

    # Combine the data into a single list
    combined_data = []
    for user_profile in user_profiles_filtered:
        combined_data.append({
            'customer_id': user_profile['customer_id'],
            'full_name': user_profile['full_name'],
            'email_user': user_profile['email_user'],
            'usertype': user_profile['usertype'],
            'account_name': user_profile['account_name'],
            'account_type': user_profile['account_type'],
            'account_number': user_profile['account_number'],
            'bank_name': user_profile['bank_name'],
            'bank_id': user_profile['bank_id'],
            'account_bank_branch': user_profile['account_bank_branch']
        })

    return combined_data






@anvil.server.callable
def update_fin_platform_fees():
    # Step 1: Calculate the number of lenders
    num_lenders = len(app_tables.fin_user_profile.search(usertype='lender'))
    
    # Step 2: Calculate the number of borrowers
    num_borrowers = len(app_tables.fin_user_profile.search(usertype='borrower'))
    
    # Step 3: Calculate the number of products
    num_products = len(app_tables.fin_product_details.search())

    # Step 4: Calculate the total amount invested by lenders
    total_lenders_invested = sum(lender['lender_total_commitments'] or 0 for lender in app_tables.fin_lender.search())

    # Step 5: Calculate the number of unique borrowers who have taken a loan
    borrower_ids = set()
    for loan in app_tables.fin_loan_details.search():
        borrower_ids.add(loan['borrower_customer_id'])
    total_borrowers_loan_taken = len(borrower_ids)
    
    # Step 6: Determine the most used product name
    product_usage = {}
    for loan in app_tables.fin_loan_details.search():
        product_name = loan['product_name']
        if product_name in product_usage:
            product_usage[product_name] += 1
        else:
            product_usage[product_name] = 1
    
    # If no loans found, handle it gracefully
    if not product_usage:
        return "No loans found to determine the most used product."
    
    # Find the product name with the highest count
    most_used_product_name = max(product_usage, key=product_usage.get)
    
    # Step 7: Update the fin_platform_fees table
    fee_record = app_tables.fin_platform_details.get()  # Assuming there's only one record, or adapt as needed

    # If no fee record exists, add a new row
    if fee_record is None:
        fee_record = app_tables.fin_platform_details.add_row()
    
    fee_record.update(
        total_lenders=num_lenders,
        total_borrowers=num_borrowers,
        total_products_count=num_products,
        most_used_product=most_used_product_name,
        total_borrowers_loan_taken=total_borrowers_loan_taken,
        total_lenders_invested=total_lenders_invested
    )

    # return "Platform fees updated successfully."




# @anvil.server.callable
# def update_fin_platform_fees():
#     # Step 1: Calculate the number of lenders
#     num_lenders = len(app_tables.fin_user_profile.search(usertype='lender'))
    
#     # Step 2: Calculate the number of borrowers
#     num_borrowers = len(app_tables.fin_user_profile.search(usertype='borrower'))
    
#     # Step 3: Calculate the number of products
#     num_products = len(app_tables.fin_product_details.search())

#     total_borrowers_loan_taken = len(app_tables.fin_loan_details.search())
    
#     # Step 4: Determine the most used product name
#     product_usage = {}
#     for loan in app_tables.fin_loan_details.search():
#         product_name = loan['product_name']
#         if product_name in product_usage:
#             product_usage[product_name] += 1
#         else:
#             product_usage[product_name] = 1
    
#     # If no loans found, handle it gracefully
#     if not product_usage:
#         return "No loans found to determine the most used product."
    
#     # Find the product name with the highest count
#     most_used_product_name = max(product_usage, key=product_usage.get)
    
#     # Step 5: Update the fin_platform_fees table
#     fee_record = app_tables.fin_platform_details.get()  # Assuming there's only one record, or adapt as needed

#     # If no fee record exists, add a new row
#     if fee_record is None:
#         fee_record = app_tables.fin_platform_details.add_row()
    
#     fee_record.update(
#         total_lenders=num_lenders,
#         total_borrowers=num_borrowers,
#         total_products_count=num_products,
#         most_used_product=most_used_product_name,
#         total_borrowers_loan_taken = total_borrowers_loan_taken
#     )
@anvil.server.callable
def update_eod_report():
    today_date = datetime.now().date()
    all_payments = app_tables.fin_emi_table.search()
    
    payments_today = [payment for payment in all_payments if payment['scheduled_payment_made'].date() == today_date]
    
    total_amount_received = sum(payment['amount_paid'] for payment in payments_today)
    total_platform_amount = sum(payment['total_platform_fee'] for payment in payments_today)
    total_lender_share = sum(payment['lender_returns'] for payment in payments_today)
    
    eod_report = app_tables.fin_eod_reports.get(date=today_date)
    if eod_report is None:
        eod_report = app_tables.fin_eod_reports.add_row(date=today_date, total_amount_received=0, total_platform_share=0, total_lender_share=0)
    
    eod_report['total_amount_received'] = total_amount_received
    eod_report['total_platform_share'] = total_platform_amount
    eod_report['total_lender_share'] = total_lender_share
    eod_report.update()

@anvil.server.background_task
def update_eod_report_1():
    today_date = datetime.now().date()
    all_payments = app_tables.fin_emi_table.search()
    
    payments_today = [payment for payment in all_payments if payment['scheduled_payment_made'].date() == today_date]
    
    total_amount_received = sum(payment['amount_paid'] for payment in payments_today)
    total_platform_amount = sum(payment['total_platform_fee'] for payment in payments_today)
    total_lender_share = sum(payment['lender_returns'] for payment in payments_today)
    
    eod_report = app_tables.fin_eod_reports.get(date=today_date)
    if eod_report is None:
        eod_report = app_tables.fin_eod_reports.add_row(date=today_date, total_amount_received=0, total_platform_share=0, total_lender_share=0)
    
    eod_report['total_amount_received'] = total_amount_received
    eod_report['total_platform_share'] = total_platform_amount
    eod_report['total_lender_share'] = total_lender_share
    eod_report.update()