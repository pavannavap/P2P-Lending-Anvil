from ._anvil_designer import borrower_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class borrower_profile(borrower_profileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user_id=main_form_module.userId
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_profile=app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_profile: 
      self.label_1.text=user_profile['full_name']
      self.email.text=user_profile['email_user']
      self.mobile.text=user_profile['mobile']
      self.birh.text=user_profile['date_of_birth']
      self.city.text=user_profile['city']
      # self.pan_text.text=user_profile['pan_number']
      self.gender.text=user_profile['gender']
      # self.language.text=user_profile['mouther_tounge']
      self.image_1.source = user_profile['user_photo']
      self.status.text=user_profile['marital_status']
    # Any code you write here will run before the form opens.

  # def button_1_click(self, **event_args):
  #   user_profile=app_tables.user_profile.get(customer_id=self.user_id)
  #   if user_profile: 
  #    user_profile['full_name']=self.borrower_full_name_text.text
  #    user_profile['email_user']=self.mail_text.text
  #    user_profile['mobile']=self.mobile_text.text
  #    user_profile['date_of_birth']=self.date_label.text
  #    user_profile['city']=self.city_text.text
  #    user_profile['pan_number']=self.pan_text.text
  #    user_profile['gender']=self.gender_down.text
  #    user_profile['mouther_tounge']=self.mother_label.text
  #    user_profile.update()
  #   alert('saved sucessfully')
  #   open_form('borrower_registration_form.dashboard')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard.edit_profile')



