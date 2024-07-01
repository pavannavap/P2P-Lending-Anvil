# from ._anvil_designer import risk_poolTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import plotly.graph_objects as go

# class risk_pool(risk_poolTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     self.repeating_panel_1.items = []
#     self.all_items = []

#     # Aggregate counts for all risk levels and initialize plot
#     self.aggregate_counts()
#     self.initialize_plot()

#   def aggregate_counts(self):
#     """Aggregate the counts of loans for each risk level"""
#     self.low_risk_count = len(self.get_filtered_rows("lapsed fee"))
#     self.medium_risk_count = len(self.get_filtered_rows("default fee"))
#     self.high_risk_count = len(self.get_filtered_rows("NPA fee"))

#   def get_filtered_rows(self, risk_level):
#     """Fetch and filter rows from EMI table based on risk level"""
#     lapsed_settings = app_tables.fin_loan_settings.get(loans=risk_level)
#     min_days = lapsed_settings['minimum_days']
#     max_days = lapsed_settings['maximum_days']
#     emi_rows = app_tables.fin_emi_table.search()
#     return [row for row in emi_rows if min_days <= row['days_left'] <= max_days]

#   def initialize_plot(self):
#     """Initialize the plot with aggregated counts"""
#     fig = go.Figure(data=[
#       go.Bar(name='Low Risk', x=['Low Risk'], y=[self.low_risk_count], marker_color='green'),
#       go.Bar(name='Medium Risk', x=['Medium Risk'], y=[self.medium_risk_count], marker_color='orange'),
#       go.Bar(name='High Risk', x=['High Risk'], y=[self.high_risk_count], marker_color='red')
#     ])
    
#     fig.update_layout(title='Loan Risk Distribution',
#                       xaxis_title='Risk Level',
#                       yaxis_title='Number of Loans',
#                       barmode='group')
    
#     self.risk_plot.data = fig.data
#     self.risk_plot.layout = fig.layout

#   def update_plot(self):
#     """Update the plot with the current risk data"""
#     fig = go.Figure(data=[
#       go.Bar(name='Low Risk', x=['Low Risk'], y=[self.low_risk_count], marker_color='green'),
#       go.Bar(name='Medium Risk', x=['Medium Risk'], y=[self.medium_risk_count], marker_color='orange'),
#       go.Bar(name='High Risk', x=['High Risk'], y=[self.high_risk_count], marker_color='red')
#     ])
    
#     fig.update_layout(title='Loan Risk Distribution',
#                       xaxis_title='Risk Level',
#                       yaxis_title='Number of Loans',
#                       barmode='group')
    
#     self.risk_plot.data = fig.data
#     self.risk_plot.layout = fig.layout

#   def button_low_risk_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     self.text_box_search.text = ""
#     filtered_rows = self.get_filtered_rows("lapsed fee")

#     # Set the filtered rows to the repeating panel
#     result = []
#     for row in filtered_rows:
#       loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
#       if loan_details:
#         combined_data = {
#           'emi_number': row['emi_number'],
#           'days_left': row['days_left'],
#           'loan_id': row['loan_id'],
#           'lender_email': row['lender_email'],
#           'borrower_customer_id': row['borrower_customer_id'],
#           'product_name': loan_details['product_name'],
#           'borrower_email': row['borrower_email'],
#           'borrower_full_name': loan_details['borrower_full_name']
#         }
#         result.append(combined_data)
#     self.all_items = result
#     self.repeating_panel_1.items = result
#     self.text_box_search.placeholder = 'Search low risk loans'
#     self.label.visible = True
#     self.label.text = 'Low Risk loans'
#     self.data_grid_1.visible = True
#     self.column_panel_1.visible = True
#     self.data_grid_2.visible = False

#     # Update the plot
#     # self.aggregate_counts()
#     # self.update_plot()

#   def button_medium_risk_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     self.text_box_search.text = ""
#     filtered_rows = self.get_filtered_rows("default fee")
  
#     # Fetch additional details from the loan details table
#     result = []
#     for row in filtered_rows:
#       loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
#       if loan_details:
#         combined_data = {
#           'emi_number': row['emi_number'],
#           'days_left': row['days_left'],
#           'loan_id': row['loan_id'],
#           'lender_email': row['lender_email'],
#           'borrower_customer_id': row['borrower_customer_id'],
#           'product_name': loan_details['product_name'],
#           'borrower_email': row['borrower_email'],
#           'borrower_full_name': loan_details['borrower_full_name']
#         }
#         result.append(combined_data)
#     self.all_items = result
#     self.repeating_panel_1.items = result
#     self.text_box_search.placeholder = ' Search medium risk loans'
#     self.label.visible = True
#     self.label.text = 'Medium Risk loans'
#     self.data_grid_1.visible = True
#     self.column_panel_1.visible = True
#     self.data_grid_2.visible = False
    
#     # Update the plot
#     # self.aggregate_counts()
#     # self.update_plot()

#   def button_high_risk_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     self.text_box_search.text = ""
#     filtered_rows = self.get_filtered_rows("NPA fee")
  
#     # Fetch additional details from the loan details table
#     result = []
#     for row in filtered_rows:
#       loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
#       if loan_details:
#         combined_data = {
#           'emi_number': row['emi_number'],
#           'days_left': row['days_left'],
#           'loan_id': row['loan_id'],
#           'lender_email': row['lender_email'],
#           'borrower_customer_id': row['borrower_customer_id'],
#           'product_name': loan_details['product_name'],
#           'borrower_full_name': loan_details['borrower_full_name'],
#           'borrower_email': row['borrower_email'],
#         }
#         result.append(combined_data)
#     self.all_items = result
#     self.repeating_panel_1.items = result
#     self.text_box_search.placeholder = 'Search high risk loans'
#     self.label.visible = True
#     self.label.text = 'High Risk loans'
#     self.data_grid_1.visible = True
#     self.column_panel_1.visible = True
#     self.data_grid_2.visible = False
      
#     # Update the plot
#     # self.aggregate_counts()
#     # self.update_plot()

#   def search_button_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     search_text = self.text_box_search.text.strip().lower()
#     if search_text:
#       # Filter items based on search text
#       filtered_items = [
#         item for item in self.all_items
#         if (search_text in str(item['emi_number']).lower() or
#             search_text in str(item['borrower_customer_id']).lower() or
#             search_text in item['product_name'].lower() or
#             search_text in item['borrower_full_name'].lower()or
#             search_text in item['borrower_email'].lower())
#       ]
#       self.suggestions_panel.items = filtered_items
#       self.data_grid_2.visible = True
#       self.data_grid_1.visible = False
#     else:
#       self.suggestions_panel.items = []
#       self.data_grid_2.visible = False
#       self.data_grid_1.visible = True

#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('admin.dashboard.reporting_and_analytical_modules')



from ._anvil_designer import risk_poolTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class risk_pool(risk_poolTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.repeating_panel_1.items = []
        self.all_items = []

        # Initialize plot with placeholder data
        self.initialize_plot()

    def aggregate_counts(self):
        """Aggregate the counts of loans for each risk level"""
        self.low_risk_count = len(self.get_filtered_rows("lapsed fee"))
        self.medium_risk_count = len(self.get_filtered_rows("default fee"))
        self.high_risk_count = len(self.get_filtered_rows("NPA fee"))

    def get_filtered_rows(self, risk_level):
        """Fetch and filter rows from EMI table based on risk level"""
        lapsed_settings = app_tables.fin_loan_settings.get(loans=risk_level)
        min_days = lapsed_settings['minimum_days']
        max_days = lapsed_settings['maximum_days']
        emi_rows = app_tables.fin_emi_table.search()
        return [row for row in emi_rows if min_days <= row['days_left'] <= max_days]

    def initialize_plot(self):
        """Initialize the plot with placeholder data"""
        fig = go.Figure(data=[
            go.Bar(name='Low Risk', x=['Low Risk'], y=[0], marker_color='green'),
            go.Bar(name='Medium Risk', x=['Medium Risk'], y=[0], marker_color='orange'),
            go.Bar(name='High Risk', x=['High Risk'], y=[0], marker_color='red')
        ])

        fig.update_layout(title='Loan Risk Distribution',
                          xaxis_title='Risk Level',
                          yaxis_title='Number of Loans',
                          barmode='group')

        self.risk_plot.data = fig.data
        self.risk_plot.layout = fig.layout

    def update_plot(self):
        """Update the plot with the current risk data"""
        self.aggregate_counts()

        fig = go.Figure(data=[
            go.Bar(name='Low Risk', x=['Low Risk'], y=[self.low_risk_count], marker_color='green'),
            go.Bar(name='Medium Risk', x=['Medium Risk'], y=[self.medium_risk_count], marker_color='orange'),
            go.Bar(name='High Risk', x=['High Risk'], y=[self.high_risk_count], marker_color='red')
        ])

        fig.update_layout(title='Loan Risk Distribution',
                          xaxis_title='Risk Level',
                          yaxis_title='Number of Loans',
                          barmode='group')

        self.risk_plot.data = fig.data
        self.risk_plot.layout = fig.layout

    def button_low_risk_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_search.text = ""
        filtered_rows = self.get_filtered_rows("lapsed fee")

        # Set the filtered rows to the repeating panel
        result = []
        for row in filtered_rows:
            loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
            if loan_details:
                combined_data = {
                    'emi_number': row['emi_number'],
                    'days_left': row['days_left'],
                    'loan_id': row['loan_id'],
                    'lender_email': row['lender_email'],
                    'borrower_customer_id': row['borrower_customer_id'],
                    'product_name': loan_details['product_name'],
                    'borrower_email': row['borrower_email'],
                    'borrower_full_name': loan_details['borrower_full_name']
                }
                result.append(combined_data)
        self.all_items = result
        self.repeating_panel_1.items = result
        self.text_box_search.placeholder = 'Search low risk loans'
        self.label.visible = True
        self.label.text = 'Low Risk loans'
        self.data_grid_1.visible = True
        self.column_panel_1.visible = True
        self.data_grid_2.visible = False

        # Update the plot
        self.update_plot()

    def button_medium_risk_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_search.text = ""
        filtered_rows = self.get_filtered_rows("default fee")

        # Fetch additional details from the loan details table
        result = []
        for row in filtered_rows:
            loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
            if loan_details:
                combined_data = {
                    'emi_number': row['emi_number'],
                    'days_left': row['days_left'],
                    'loan_id': row['loan_id'],
                    'lender_email': row['lender_email'],
                    'borrower_customer_id': row['borrower_customer_id'],
                    'product_name': loan_details['product_name'],
                    'borrower_email': row['borrower_email'],
                    'borrower_full_name': loan_details['borrower_full_name']
                }
                result.append(combined_data)
        self.all_items = result
        self.repeating_panel_1.items = result
        self.text_box_search.placeholder = ' Search medium risk loans'
        self.label.visible = True
        self.label.text = 'Medium Risk loans'
        self.data_grid_1.visible = True
        self.column_panel_1.visible = True
        self.data_grid_2.visible = False

        # Update the plot
        self.update_plot()

    def button_high_risk_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_search.text = ""
        filtered_rows = self.get_filtered_rows("NPA fee")

        # Fetch additional details from the loan details table
        result = []
        for row in filtered_rows:
            loan_details = app_tables.fin_loan_details.get(loan_id=row['loan_id'])
            if loan_details:
                combined_data = {
                    'emi_number': row['emi_number'],
                    'days_left': row['days_left'],
                    'loan_id': row['loan_id'],
                    'lender_email': row['lender_email'],
                    'borrower_customer_id': row['borrower_customer_id'],
                    'product_name': loan_details['product_name'],
                    'borrower_full_name': loan_details['borrower_full_name'],
                    'borrower_email': loan_details['borrower_email'],
                }
                result.append(combined_data)
        self.all_items = result
        self.repeating_panel_1.items = result
        self.text_box_search.placeholder = 'Search high risk loans'
        self.label.visible = True
        self.label.text = 'High Risk loans'
        self.data_grid_1.visible = True
        self.column_panel_1.visible = True
        self.data_grid_2.visible = False

        # Update the plot
        self.update_plot()

    def search_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        search_text = self.text_box_search.text.strip().lower()
        if search_text:
            # Filter items based on search text
            filtered_items = [
                item for item in self.all_items
                if (search_text in str(item['emi_number']).lower() or
                    search_text in str(item['borrower_customer_id']).lower() or
                    search_text in item['product_name'].lower() or
                    search_text in item['borrower_full_name'].lower() or
                    search_text in item['borrower_email'].lower())
            ]
            self.suggestions_panel.items = filtered_items
            self.data_grid_2.visible = True
            self.data_grid_1.visible = False
        else:
            self.suggestions_panel.items = []
            self.data_grid_2.visible = False
            self.data_grid_1.visible = True

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.reporting_and_analytical_modules')
