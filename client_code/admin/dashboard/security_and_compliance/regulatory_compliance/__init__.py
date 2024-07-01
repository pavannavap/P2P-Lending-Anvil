from ._anvil_designer import regulatory_complianceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class regulatory_compliance(regulatory_complianceTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.fetch_and_display_data()
        self.button_1.text = "Email Verified"
        self.label_2.visible = False

    def fetch_and_display_data(self):
        # Fetch all user profiles from the fin_user_profile table
        user_profiles = app_tables.fin_user_profile.search()
        
        verified_users = []
        unverified_users = []
        
        # Iterate through each user profile
        for profile in user_profiles:
            # Fetch corresponding user record from the users table based on email
            user_record = app_tables.users.get(email=profile['email_user'])
            
            if user_record:
                # Collect necessary details from both tables
                user_data = {
                    'email_user': profile['email_user'],
                    'full_name': profile['full_name'],
                    'mobile': profile['mobile'],
                    'customer_id': profile['customer_id'],
                    'usertype': profile['usertype'],
                    'signed_up': user_record['signed_up'],
                    'email_verified': user_record['email_verified']
                }

                # Append to the appropriate list based on email_verified
                if user_record['email_verified']:
                    verified_users.append(user_data)
                else:
                    unverified_users.append(user_data)
        
        # Display user profile data in the appropriate repeating panels
        self.repeating_panel_verified.items = verified_users
        self.repeating_panel_unverified.items = unverified_users

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      if self.button_1.text == "Email Verified":
            self.button_1.text = "Email Unverified"
            self.data_grid_1.visible = True
            self.data_grid_2.visible = False
            self.label_2.visible = False
            self.label_1.visible = True
      else:
            self.button_1.text = "Email Verified"
            self.data_grid_1.visible = False
            self.data_grid_2.visible = True
            self.label_2.visible = True
            self.label_1.visible = False

    def back_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.security_and_compliance')


