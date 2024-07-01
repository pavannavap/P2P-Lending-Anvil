from ._anvil_designer import main_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
from ..user_form import user_module 
from . import main_form_module
# from ..borrower_dashboard import borrower_main_form_module
# from ...borrower_registration_form.dashboard import main_form_module
from ...borrower.dashboard import main_form_module

class main_form(main_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # Set up event handlers
    # self.button_1_click_event = self.button_1_click
    self.dropdown_change_event = self.drop_down_1_change
    # Set up event handlers
    # dropdown_items = ["Invest Now", "Apply for Loan"]
    # for item in dropdown_items:
    #     Label = Label(text=item, role='dropdown_item', visible=False, **properties)
    #     Label.set_event_handler('x-click', self.dropdown_item_click)
    #     self.add_component(Label)
        
    #     # Set up event handlers
    #     self.button_2_click_event = self.button_2_click
  
  def login_signup_button_click(self, **event_args):
    open_form('bank_users.main_form.login_page')
        # anvil.users.login_with_form()
        # current_user = anvil.users.get_user()
        # if current_user:
        #     user_email = current_user['email']
        #     print(user_email)
        #     check_user_already_exist = user_module.check_user_profile(user_email)
        #     print(check_user_already_exist)
        #     if check_user_already_exist is None:
        #         print("main if statement was executed")
        #         user_module.add_email_and_user_id(user_email)
        #         main_form_module.email = user_email
        #         main_form_module.flag = True
        #         main_form_module.userId = userid
        #         open_form('bank_users.main_form.basic_registration_form')
        #     else:
        #         check_user_registration = user_module.check_user_registration_form_done_or_not_engine(user_email)
        #         print("main else statement was executed")
        #         user_profile_e = app_tables.fin_user_profile.get(email_user=user_email)
        #         main_form_module.email = user_email
        #         main_form_module.userId = user_module.find_user_id(user_email)
        #         self.user_id =  user_module.find_user_id(user_email)
        #         userid = self.user_id
                
        #         if user_profile_e is not None:
        #             user_type = user_profile_e['usertype']
        #             last_confirm = user_profile_e['last_confirm']
        #             marital_status = user_profile_e['marital_status']
        #             actual_count=user_profile_e['form_count']
        #             print(actual_count)
        #             print("")
        #             if user_type == 'admin' or user_type == 'super admin':
        #                 open_form('admin.dashboard')
        #             elif user_type == 'lender' and last_confirm:
        #                 open_form('lendor_registration_form.dashboard')
        #             elif user_type == 'borrower' and last_confirm:
        #                 if user_profile_e['one_time_settlement'] != True:
        #                     open_form('borrower_registration_form.dashboard')
        #                 elif user_profile_e['one_time_settlement'] == True:
        #                     open_form('borrower_registration_form.ots_dashboard')
        #             elif actual_count is not None and actual_count == 0:
        #               open_form('bank_users.user_form')
        #             # For Borrower Registration Form  
        #             elif user_type == 'borrower' and actual_count==1:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==1.1:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_10th_class',user_id=userid) 
        #             elif user_type == 'borrower' and actual_count==1.2:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_intermediate',user_id=userid) 
        #             elif user_type == 'borrower' and actual_count==1.3:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_btech',user_id=userid)   
        #             elif user_type == 'borrower' and actual_count==1.4:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_mtech',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==1.5:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_phd',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.1:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_student',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.2:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_self_employment',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.21:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.22:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_2',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.23:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_3',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.31:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_1',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.32:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.33:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==2.4:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_farmer',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==3:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==3.1:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital.star_1_borrower_registration_form_3_marital_married',user_id=userid, marital_status = marital_status)
        #             elif user_type == 'borrower' and actual_count==4:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_4_loan',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==5:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_5_bank_1',user_id=userid)
        #             elif user_type == 'borrower' and actual_count==6:
        #               open_form('borrower_registration_form.star_1_borrower_registration_form_5_bank_2',user_id=userid)
        #             # For Lender Registration Form  
        #             elif user_type == 'lender' and actual_count==1:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form',user_id=userid)
        #             elif user_type == 'lender' and actual_count==1.1:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_10th_class',user_id=userid) 
        #             elif user_type == 'lender' and actual_count==1.2:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Intermediate',user_id=userid) 
        #             elif user_type == 'lender' and actual_count==1.3:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Btech',user_id=userid)   
        #             elif user_type == 'lender' and actual_count==1.4:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Mtech',user_id=userid)
        #             elif user_type == 'lender' and actual_count==1.5:
        #                open_form('lendor_registration_form.lender_registration_form_1_education_form.lender_registration_education_Phd',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2:
        #                open_form('lendor_registration_form.lender_registration_form_2',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.21:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_1',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.22:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_2',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.23:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_Institutional_form_3',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.31:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_individual_form_1',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.32:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_individual_form_2',user_id=userid)
        #             elif user_type == 'lender' and actual_count==2.33:
        #                open_form('lendor_registration_form.lender_registration_form_2.lender_registration_individual_form_3',user_id=userid)
        #             elif user_type == 'lender' and actual_count==3:
        #                open_form('lendor_registration_form.lender_registration_form_3_marital_details',user_id=userid)
        #             elif user_type == 'lender' and actual_count==3.1:
        #                open_form('lendor_registration_form.lender_registration_form_3_marital_details.lender_registration_form_3_marital_married',user_id=userid,marital_status = marital_status)
        #             elif actual_count==4:
        #                open_form('lendor_registration_form.lender_registration_form_4_bank_form_1',user_id=userid)
        #             elif actual_count==5:
        #                open_form('lendor_registration_form.lender_registration_form_4_bank_form_2',user_id=userid)
     
        #             else:
        #                 open_form('bank_users.main_form.basic_registration_form')
        #         else:
        #             # Handle the case when user_profile_e is None
        #             open_form('bank_users.user_form')
        # else:
        #     # Handle the case when current_user is None
        #     open_form('bank_users.user_form')

#-- imp logic dont go up--#

  
  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.about_main_form")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.products_main_form")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.contact_main_form")



  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("admin.user_issue.user_bugreports")

  def outlined_button_1_copy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.login_signup_button_click()

  def outlined_button_2_copy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.login_signup_button_click()

  # def image_9_mouse_enter(self, x, y, **event_args):
  #   """This method is called when the mouse cursor enters this component"""
  #   self.data_row_panel.background_color = '#05264d'

  # def image_9_mouse_leave(self, x, y, **event_args):
  #   """This method is called when the mouse cursor leaves this component"""
  #   self.data_row_panel.background_color = None

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rich_text_1.visible = not self.rich_text_1.visible

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rich_text_2.visible = not self.rich_text_2.visible



  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.about_main_form")

  def button_4_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rich_text_4.visible = not self.rich_text_4.visible

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rich_text_3.visible = not self.rich_text_3.visible



  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_option = self.drop_down_1.selected_value
    if selected_option == "Invest Now":
        open_form('bank_users.main_form.basic_registration_form')  # Replace 'Form1' with the name of your target form
    elif selected_option == "Apply for Loan":
        open_form('bank_users.main_form.about_main_form')

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("bank_users.main_form.contact_main_form")

  def link_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_issue.user_bugreports')

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.products_main_form')

  def button_10_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.signup_page', user_type='borrower')

  def button_10_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.investNow_applyForLoan')

  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.signup_page', user_type='borrower')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.signup_page', user_type='lender')

  def button_11_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.signup_page', user_type='lender')

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.investNow_applyForLoan')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.investNow_applyForLoan')

 


  

  






