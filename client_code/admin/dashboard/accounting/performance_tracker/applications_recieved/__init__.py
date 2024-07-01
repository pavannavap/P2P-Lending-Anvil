from ._anvil_designer import applications_recievedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class applications_recieved(applications_recievedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_1.items = ['', 'daily', 'monthly']
    self.column_panel_1.visible = False  # Ensure column_panel_1 is initially hidden
    self.column_panel_2.visible = False  # Ensure column_panel_2 is initially hidden

  def date_picker_1_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.selected_date = self.date_picker_1.date
    print("Selected date:", self.selected_date)

    if self.selected_date:
        # Fetch loans from the database
        loans = app_tables.fin_loan_details.search()
                
        # Initialize an empty list to store filtered loans
        filtered_loans = []

        for loan in loans:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
                    
            if user_profile is not None and loan['loan_updated_status'] in ["under process"]:
                # Directly compare loan['borrower_loan_created_timestamp'] with self.selected_date
                if loan['borrower_loan_created_timestamp'] == self.selected_date: 
                    filtered_loans.append({
                            'user_photo': user_profile['user_photo'],
                            'borrower_full_name': loan['borrower_full_name'],
                            'borrower_email_id': loan['borrower_email_id'],
                            'lender_full_name': loan['lender_full_name'],
                            'lender_email_id': loan['lender_email_id'],
                            'ascend_score': user_profile['ascend_value'],
                            'loan_amount': loan['loan_amount'],
                            'loan_updated_status': loan['loan_updated_status'],
                            'loan_id': loan['loan_id'],
                            'total_repayment_amount': loan['total_repayment_amount'],
                            'membership_type': loan['membership_type'],
                            'product_name': loan['product_name'],
                            'borrower_loan_created_timestamp': loan['borrower_loan_created_timestamp'],
                    })
                         
                
        if not filtered_loans:
            Notification(f"No Loans with status 'under process' found for {self.selected_date}!").show()
            self.data_grid_1.visible = False  # Hide the DataGrid if no loans found
        else:
            # Update RepeatingPanel with filtered results
            self.repeating_panel_1.items = filtered_loans
            self.data_grid_1.visible = True  # Make the DataGrid visible

  def date_picker_2_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.selected_month = self.date_picker_2.date
    print("Selected month:", self.selected_month)

    if self.selected_month:
        # Fetch loans from the database
        loans = app_tables.fin_loan_details.search()
                
        # Initialize an empty list to store filtered loans
        filtered_loans = []

        for loan in loans:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
                    
            if user_profile is not None and loan['loan_updated_status'] in ["under process"]:
                # Compare the month and year of loan['borrower_loan_created_timestamp'] with self.selected_month
                if loan['borrower_loan_created_timestamp'].month == self.selected_month.month and loan['borrower_loan_created_timestamp'].year == self.selected_month.year: 
                    filtered_loans.append({
                            'user_photo': user_profile['user_photo'],
                            'borrower_full_name': loan['borrower_full_name'],
                            'borrower_email_id': loan['borrower_email_id'],
                            'lender_full_name': loan['lender_full_name'],
                            'lender_email_id': loan['lender_email_id'],
                            'ascend_score': user_profile['ascend_value'],
                            'loan_amount': loan['loan_amount'],
                            'loan_updated_status': loan['loan_updated_status'],
                            'loan_id': loan['loan_id'],
                            'total_repayment_amount': loan['total_repayment_amount'],
                            'membership_type': loan['membership_type'],
                            'product_name': loan['product_name'],
                            'borrower_loan_created_timestamp': loan['borrower_loan_created_timestamp'],
                    })
                         
                
        if not filtered_loans:
            Notification(f"No Loans with status 'under process' found for {self.selected_month}!").show()
            self.data_grid_2.visible = False  # Hide the DataGrid if no loans found
        else:
            # Update RepeatingPanel with filtered results
            self.repeating_panel_2.items = filtered_loans
            self.data_grid_2.visible = True  # Make the DataGrid visible

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_filter = self.drop_down_1.selected_value
    print("Selected filter:", selected_filter)  # Debugging print
        
    if selected_filter == 'daily':
        self.column_panel_1.visible = True      # Make the column_panel_1 visible
        self.column_panel_2.visible = False     # Hide column_panel_2
        self.update_daily_panel()
    elif selected_filter == 'monthly':
        self.column_panel_1.visible = False     # Hide the column_panel_1
        self.column_panel_2.visible = True      # Make the column_panel_2 visible
        self.update_monthly_panel()
    else:
        self.column_panel_1.visible = False     # Hide both panels if neither 'daily' nor 'monthly' is selected
        self.column_panel_2.visible = False

  def update_daily_panel(self):
      # Your implementation for updating the daily panel
      pass

  def update_monthly_panel(self):
      # Your implementation for updating the monthly panel
      pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.performance_tracker')

              

