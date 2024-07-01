from ._anvil_designer import dashboard_report_a_problemTemplate
from anvil import *
import anvil.server
import datetime
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from .. import main_form_module as main_form_module

class dashboard_report_a_problem(dashboard_report_a_problemTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.user_id = main_form_module.userId
        print(self.user_id)
        user_profile = app_tables.fin_user_profile.get(customer_id=self.user_id)
      
        if user_profile:
            self.name_box.text = user_profile['full_name']
            self.mobile_box.text = user_profile['mobile']
            self.email_box.text = user_profile['email_user']
          

        self.usertype = properties.get('usertype', 'borrower')  # Default value is 'borrower'
        # Populate dropdowns or other components here
        self.subcategory = app_tables.fin_report_issue_category.search()
        self.category = app_tables.fin_issue_category.search()
        self.drop_down_1.items = [(c['issue_category'], c['issue_category']) for c in self.category]
        self.drop_down_1.selected_value = self.category[0]['issue_category']  # Set default value
        # Set up event handler for category dropdown change
        self.drop_down_1.set_event_handler('change', self.update_subcategory)

        # Call the update_subcategory method to initialize the subcategory dropdown
        self.update_subcategory()

    def update_subcategory(self, **event_args):
        selected_category = self.drop_down_1.selected_value
        if selected_category == 'Loan Issue':
            self.drop_down_2.items = [(sli['borrower_subcategory_loan_issue'], sli['borrower_subcategory_loan_issue']) for sli in self.subcategory]
        elif selected_category == 'Technical Issue':
            self.drop_down_2.items = [(sti['subcategory_technical_issue'], sti['subcategory_technical_issue']) for sti in self.subcategory]
        else:
            self.drop_down_2.items = [(sli['lendor_subcategory_loan_issue'], sli['lendor_subcategory_loan_issue']) for sli in self.subcategory]



    def button_2_click(self, **event_args):
        # Get input values from text boxes
        full_name = self.name_box.text
        mobile = self.mobile_box.text
        email_id = self.email_box.text
        category = self.drop_down_1.selected_value
        subcategory = self.drop_down_2.selected_value
        description = self.description_box.text

        # Validate if all required fields are filled
        if not full_name or not mobile or not email_id or not category or not subcategory or not description:
            alert("Please fill in all required fields.")
            return
  
        # Validate mobile number
        try:
            mobile = int(mobile)
        except ValueError:
            alert("Mobile number must be a valid number.")
            return

        # Check if a file is uploaded
        if not self.file_loader_1.file:
            alert("Please upload a file.")
            return

        current_datetime = datetime.datetime.now()

        # Get the file uploaded via file_loader_1
        issue_photo = self.file_loader_1.file
        # Check if the checkbox is checked
        it_is_urgent = self.check_box_1.checked

        # Add a row to the fin_reported_problems table with file details
        app_tables.fin_reported_problems.add_row(name=full_name,
                                                 email=email_id,
                                                 mobile_number=mobile,
                                                 category=category,
                                                 subcategory=subcategory,
                                                 issue_description=description,
                                                 report_date=current_datetime,
                                                 issue_photo=issue_photo,
                                                 it_is_urgent=it_is_urgent,
                                                 usertype=self.usertype)

        # Show success message to the user
        alert('Problem reported successfully. Thank you for your feedback!')

        # Open dashboard form or any other form
        # customer_id = self.user_id
        open_form('borrower.dashboard' if self.usertype == 'borrower' else 'lender.dashboard')

    def image_1_copy_2_mouse_up(self, x, y, button, **event_args):
        """This method is called when a mouse button is released on this component"""
        open_form('borrower.dashboard.dashboard_report_a_problem')


    def file_loader_1_change(self, file, **event_args):
      """This method is called when a new file is loaded into this FileLoader"""
      self.image_issue.source = file




