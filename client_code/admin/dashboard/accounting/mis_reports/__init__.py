# from ._anvil_designer import mis_reportsTemplate
# from anvil import *
# import plotly.graph_objects as go
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class mis_reports(mis_reportsTemplate):
#     def __init__(self, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)

#         # Any code you write here will run before the form opens.
#         self.plot_data()
#         self.plot_loan_data()
#         self.create_user_bar_chart()
#         # self.create_risk_bar_chart()

#     def plot_data(self):
#         # Fetch data from tables
#         loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of('closed loan', 'rejected', 'disbursed loan'))
#         lenders = app_tables.fin_lender.search()
#         users = app_tables.fin_user_profile.search(usertype=q.any_of('lender', 'borrower'))

#         # Calculate metrics
#         no_of_loans_disbursed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'disbursed loan'])
#         no_of_loans_closed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'closed loan'])
#         no_of_loans_rejected = len([loan for loan in loan_details if loan['loan_updated_status'] == 'rejected'])
#         amount_disbursed = sum([loan['lender_returns'] for loan in loan_details])
#         no_of_borrowers = len([user for user in users if user['usertype'] == 'borrower'])
#         no_of_lenders = len([user for user in users if user['usertype'] == 'lender'])
#         lenders_commitment = sum([lender['return_on_investment'] for lender in lenders])

#         # Data for the pie chart
#         values = [
#             no_of_loans_disbursed,
#             no_of_loans_closed,
#             no_of_loans_rejected,
#             amount_disbursed,
#             no_of_borrowers,
#             no_of_lenders,
#             lenders_commitment
#         ]
#         labels = [
#             'No of Loans Disbursed: {}'.format(no_of_loans_disbursed),
#             'No of Loans Closed: {}'.format(no_of_loans_closed),
#             'No of Loans Rejected: {}'.format(no_of_loans_rejected),
#             'Amount Disbursed: {}'.format(amount_disbursed),
#             'No of Borrowers: {}'.format(no_of_borrowers),
#             'No of Lenders: {}'.format(no_of_lenders),
#             'Lenders Commitment: {}'.format(lenders_commitment)
#         ]

#         # Create the pie chart
#         fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])

#         fig.update_layout(title={'text': 'Financial Loan Details', 'font': {'size': 24, 'color': 'black', 'family': 'Arial', 'bold': True}})

#         # Embed the plot in the Anvil app
#         self.plot_1.figure = fig

#     def plot_loan_data(self):
#         # Fetch data from tables
#         loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of('closed loan', 'rejected', 'disbursed loan', 'foreclosure', 'lost opportunities', 'approved', 'under process', 'extension'))

#         # Calculate metrics
#         no_of_loans_disbursed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'disbursed loan'])
#         no_of_loans_closed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'closed loan'])
#         no_of_loans_rejected = len([loan for loan in loan_details if loan['loan_updated_status'] == 'rejected'])
#         no_of_loans_foreclosed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'foreclosure'])
#         no_of_loans_lost_opportunity = len([loan for loan in loan_details if loan['loan_updated_status'] == 'lost opportunities'])
#         no_of_loans_approved = len([loan for loan in loan_details if loan['loan_updated_status'] == 'approved'])
#         no_of_loans_under_process = len([loan for loan in loan_details if loan['loan_updated_status'] == 'under process'])
#         no_of_extension_loans = len([loan for loan in loan_details if loan['loan_updated_status'] == 'extension'])
        
#         # Data for the pie chart
#         values = [
#             no_of_loans_disbursed,
#             no_of_loans_closed,
#             no_of_loans_rejected,
#             no_of_loans_foreclosed,
#             no_of_loans_lost_opportunity,
#             no_of_loans_approved,
#             no_of_loans_under_process,
#             no_of_extension_loans
#         ]
#         labels = [
#             'No of Loans Disbursed: {}'.format(no_of_loans_disbursed),
#             'No of Loans Closed: {}'.format(no_of_loans_closed),
#             'No of Loans Rejected: {}'.format(no_of_loans_rejected),
#             'No of Loans Foreclosed: {}'.format(no_of_loans_foreclosed),
#             'No of Loans Lost Opportunity: {}'.format(no_of_loans_lost_opportunity),
#             'No of Loans Approved: {}'.format(no_of_loans_approved),
#             'No of Loans Under Process: {}'.format(no_of_loans_under_process),
#             'No of Extension Loans: {}'.format(no_of_extension_loans)
#         ]

#         # Create the pie chart
#         fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])

#         # Update layout for better appearance
#         fig.update_layout(title={'text': 'Different types of Loans', 'font': {'size': 24, 'color': 'black', 'family': 'Arial', 'bold': True}})

#         # Embed the plot in the Anvil app
#         self.plot_2.figure = fig
    
#     def create_user_bar_chart(self):
#         # Fetch investment data
#         investments = app_tables.fin_lender.search()
        
#         # Debugging: Print fetched investments
#         print(f"Fetched investments: {list(investments)}")
        
#         # Initialize a dictionary to store total return_on_investment for each customer_id
#         customer_returns = {}
        
#         for investment in investments:
#             customer_id = investment['customer_id']
#             if customer_id not in customer_returns:
#                 customer_returns[customer_id] = 0
#             customer_returns[customer_id] += investment['return_on_investment']
        
#         # Convert the dictionary to a list of tuples and sort by return_on_investment in descending order
#         sorted_returns = sorted(customer_returns.items(), key=lambda x: x[1], reverse=True)
        
#         # Prepare data for the bar chart
#         categories = [str(item[0]) for item in sorted_returns]  # customer_ids
#         values = [item[1] for item in sorted_returns]  # return_on_investments
        
#         # Create bar chart trace
#         trace = go.Bar(x=categories, y=values, marker_color='green')
        
#         # Create a layout
#         layout = go.Layout(
#             title=dict(text='Return on Investment by Customer', font=dict(size=16, weight='bold')),
#             xaxis=dict(
#                 title='Customer ID',
#                 tickfont=dict(size=10, weight='bold'),
#                 tickangle=45,
#                 type='category'  # Ensures the x-axis is treated as categorical
#             ),
#             yaxis=dict(title='Return on Investment'),
#             barmode='group'
#         )
        
#         # Create a figure
#         fig = go.Figure(data=[trace], layout=layout)
        
#         # Debugging: Print the figure to ensure it's created
#         print(f"Created figure: {fig}")
        
#         # Set the plot in the Plot component
#         self.plot_3.figure = fig
        
#         # Debugging: Check if the plot is assigned correctly
#         print(f"Assigned figure to plot_3: {self.plot_3.figure}") 


    
#     def create_risk_bar_chart(self):
#         # Fetch investment data
#         investments = app_tables.fin_lender.search()
        
#         # Debugging: Print fetched investments
#         print(f"Fetched investments: {list(investments)}")
        
#         # Initialize a dictionary to store total return_on_investment for each customer_id
#         customer_returns = {}
        
#         for investment in investments:
#             customer_id = investment['customer_id']
#             if customer_id not in customer_returns:
#                 customer_returns[customer_id] = 0
#             customer_returns[customer_id] += investment['return_on_investment']
        
#         # Convert the dictionary to a list of tuples and sort by return_on_investment in descending order
#         sorted_returns = sorted(customer_returns.items(), key=lambda x: x[1], reverse=True)
        
#         # Prepare data for the bar chart
#         categories = [str(item[0]) for item in sorted_returns]  # customer_ids
#         values = [item[1] for item in sorted_returns]  # return_on_investments
        
#         # Create bar chart trace
#         trace = go.Bar(x=categories, y=values, marker_color='green')
        
#         # Create a layout
#         layout = go.Layout(
#             title=dict(text='Return on Investment by Customer', font=dict(size=16, weight='bold')),
#             xaxis=dict(
#                 title='Customer ID',
#                 tickfont=dict(size=10, weight='bold'),
#                 tickangle=45,
#                 type='category'  # Ensures the x-axis is treated as categorical
#             ),
#             yaxis=dict(title='Return on Investment'),
#             barmode='group'
#         )
        
#         # Create a figure
#         fig = go.Figure(data=[trace], layout=layout)
        
#         # Debugging: Print the figure to ensure it's created
#         print(f"Created figure: {fig}")
        
#         # Set the plot in the Plot component
#         self.plot_4.figure = fig
        
#         # Debugging: Check if the plot is assigned correctly
#         print(f"Assigned figure to plot_4: {self.plot_4.figure}")

#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form('admin.dashboard.accounting')






from ._anvil_designer import mis_reportsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class mis_reports(mis_reportsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.plot_data()
        self.plot_loan_data()
        self.create_user_bar_chart()
        self.update_labels()

        self.aggregate_counts()
        self.initialize_plot()
        self.selected_risk_level = None

    def update_labels(self):
        # Fetch the first row from the 'fin_platform_details' table
        platform_data = app_tables.fin_platform_details.search()
        
        # Convert to list and access the first item
        platform_data_list = list(platform_data)
        
        if platform_data_list:
            first_row = platform_data_list[0]
            self.label_4.text = first_row['total_lenders']
            self.label_6.text = first_row['total_borrowers']
            self.label_10.text = first_row['total_borrowers_loan_taken']
            self.label_14.text = first_row['most_used_product']
            self.label_12.text = first_row['total_products_count']
            self.label_8.text = first_row['total_lenders_invested']
            self.label_16.text =first_row['platform_returns']
            self.link_1.text = sum(lender['return_on_investment'] for lender in app_tables.fin_lender.search())

  
    def plot_data(self):
        # Fetch data from tables
        loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of('closed loan', 'rejected', 'disbursed loan'))
        lenders = app_tables.fin_lender.search()
        users = app_tables.fin_user_profile.search(usertype=q.any_of('lender', 'borrower'))
    
        # Calculate metrics
        no_of_loans_disbursed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'disbursed loan'])
        no_of_loans_closed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'closed loan'])
        no_of_loans_rejected = len([loan for loan in loan_details if loan['loan_updated_status'] == 'rejected'])
        
        # Filter out None values for lender_share
        lender_share = sum(loan['lender_returns'] for loan in loan_details if loan['lender_returns'] is not None)
        
        no_of_borrowers = len([user for user in users if user['usertype'] == 'borrower'])
        no_of_lenders = len([user for user in users if user['usertype'] == 'lender'])
        
        # Filter out None values for lenders_commitment
        lenders_commitment = sum(lender['return_on_investment'] for lender in lenders if lender['return_on_investment'] is not None)
    
        # Data for the pie chart
        values = [
            no_of_loans_disbursed,
            no_of_loans_closed,
            no_of_loans_rejected,
            lender_share,
            no_of_borrowers,
            no_of_lenders,
            lenders_commitment
        ]
        labels = [
            'No of Loans Disbursed: {}'.format(no_of_loans_disbursed),
            'No of Loans Closed: {}'.format(no_of_loans_closed),
            'No of Loans Rejected: {}'.format(no_of_loans_rejected),
            'Lender Share: {}'.format(lender_share),
            'No of Borrowers: {}'.format(no_of_borrowers),
            'No of Lenders: {}'.format(no_of_lenders),
            'Lenders Commitment: {}'.format(lenders_commitment)
        ]
    
        # Create the pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])
    
        # Update the layout to set the size
        fig.update_layout(
            title={
                'text': 'Financial Loan Details',
                'font': {
                    'size': 20,
                    'color': 'black',
                    'family': 'Arial',
                    'bold': True
                }
            }
        )
    
        # Embed the plot in the Anvil app
        self.plot_1.figure = fig

    def plot_loan_data(self):
        # Fetch data from tables
        loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of('closed', 'rejected', 'disbursed', 'foreclosure', 'lost opportunities', 'approved', 'under process', 'extension'))
        loan_details = app_tables.fin_loan_details.search(loan_updated_status=q.any_of('closed', 'rejected', 'disbursed', 'foreclosure', 'lost opportunities', 'approved', 'under process', 'extension'))

        # Calculate metrics
        no_of_loans_disbursed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'disbursed'])
        no_of_loans_closed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'closed'])
        no_of_loans_closed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'closed'])
        no_of_loans_rejected = len([loan for loan in loan_details if loan['loan_updated_status'] == 'rejected'])
        no_of_loans_foreclosed = len([loan for loan in loan_details if loan['loan_updated_status'] == 'foreclosure'])
        no_of_loans_lost_opportunity = len([loan for loan in loan_details if loan['loan_updated_status'] == 'lost opportunities'])
        no_of_loans_approved = len([loan for loan in loan_details if loan['loan_updated_status'] == 'approved'])
        no_of_loans_under_process = len([loan for loan in loan_details if loan['loan_updated_status'] == 'under process'])
        no_of_extension_loans = len([loan for loan in loan_details if loan['loan_updated_status'] == 'extension'])
        
        # Data for the pie chart
        values = [
            no_of_loans_disbursed,
            no_of_loans_closed,
            no_of_loans_rejected,
            no_of_loans_foreclosed,
            no_of_loans_lost_opportunity,
            no_of_loans_approved,
            no_of_loans_under_process,
            no_of_extension_loans
        ]
        labels = [
            'No of Loans Disbursed: {}'.format(no_of_loans_disbursed),
            'No of Loans Closed: {}'.format(no_of_loans_closed),
            'No of Loans Rejected: {}'.format(no_of_loans_rejected),
            'No of Loans Foreclosed: {}'.format(no_of_loans_foreclosed),
            'No of Loans Lost Opportunity: {}'.format(no_of_loans_lost_opportunity),
            'No of Loans Approved: {}'.format(no_of_loans_approved),
            'No of Loans Under Process: {}'.format(no_of_loans_under_process),
            'No of Extension Loans: {}'.format(no_of_extension_loans)
        ]

        # Create the pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent')])

        # Update layout for better appearance
        fig.update_layout(title={'text': 'Different types of Loans', 'font': {'size': 24, 'color': 'black', 'family': 'Arial', 'bold': True}})
        fig.update_layout(autosize=False,width=600,height=650)
        

        # Embed the plot in the Anvil app
        self.plot_2.figure = fig
    
    def create_user_bar_chart(self):
        # Fetch investment data
        investments = app_tables.fin_lender.search()
        
        # Debugging: Print fetched investments
        print(f"Fetched investments: {list(investments)}")
        
        # Initialize a dictionary to store total return_on_investment for each customer_id
        customer_returns = {}
        
        for investment in investments:
            customer_id = investment['customer_id']
            if customer_id not in customer_returns:
                customer_returns[customer_id] = 0
            # Add the return_on_investment if it is not None
            if investment['return_on_investment'] is not None:
                customer_returns[customer_id] += investment['return_on_investment']
        
        # Convert the dictionary to a list of tuples and sort by return_on_investment in descending order
        sorted_returns = sorted(customer_returns.items(), key=lambda x: x[1], reverse=True)
        
        # Prepare data for the bar chart
        categories = [str(item[0]) for item in sorted_returns]  # customer_ids
        values = [item[1] for item in sorted_returns]  # return_on_investments
        
        # Create bar chart trace
        trace = go.Bar(
            x=categories, 
            y=values, 
            marker_color='green',
            text=[f'Rs {value}' for value in values],  # Format text
            textposition='outside'  # Display text outside the bars
        )
        
        # Create a layout
        layout = go.Layout(
            title=dict(text='Highest Return Earner by Customer', font=dict(size=16, weight='bold')),
            xaxis=dict(
                title='Customer ID',
                tickfont=dict(size=10, weight='bold'),
                tickangle=0,
                type='category'  # Ensures the x-axis is treated as categorical
            ),
            yaxis=dict(title='Return on Investment'),
            barmode='group'
        )
        
        # Create a figure
        fig = go.Figure(data=[trace], layout=layout)
        
        # Debugging: Print the figure to ensure it's created
        print(f"Created figure: {fig}")
        
        # Set the plot in the Plot component
        self.plot_3.figure = fig
        
        # Debugging: Check if the plot is assigned correctly
        print(f"Assigned figure to plot_3: {self.plot_3.figure}")

    
    
    def aggregate_counts(self):
        """Aggregate the counts of loans for each risk level"""
        # Initialize counters
        self.no_risk_count = 0
        self.low_risk_count = 0
        self.medium_risk_count = 0
        self.high_risk_count = 0
        
        # Initialize lists to store loan IDs by risk level
        self.no_risk_loans = []
        self.low_risk_loans = []
        self.medium_risk_loans = []
        self.high_risk_loans = []
        
        # Fetch all loan IDs from fin_loan_details table
        self.loan_details = list(app_tables.fin_loan_details.search())
        
        # Iterate over each loan ID and determine risk level
        for loan in self.loan_details:
            loan_id = loan['loan_id']
            if self.all_days_zero(loan_id):
                self.no_risk_count += 1
                self.no_risk_loans.append(loan)

            elif self.all_days_zero_1(loan_id):
                self.low_risk_count += 1
                self.low_risk_loans.append(loan)

            elif self.all_days_zero_2(loan_id):
                self.medium_risk_count += 1
                self.medium_risk_loans.append(loan)

            elif self.all_days_zero_3(loan_id):
                self.high_risk_count += 1
                self.high_risk_loans.append(loan)

    def all_days_zero(self, loan_id):
        """Check if all 'days_left' for a given loan_id are zero"""
        emi_details = app_tables.fin_emi_table.search(loan_id=loan_id)
        for emi in emi_details:
            if emi['days_left'] > 0:
                return False
        return True

    def all_days_zero_1(self, loan_id):
        """Check if two or more instances of 'days_left' for a given loan_id meet the condition"""
        lapsed_days = app_tables.fin_loan_settings.get(loans='lapsed fee')
        if lapsed_days:
            min_days = lapsed_days['minimum_days']
            count_valid_instances = 0
            emi_details = app_tables.fin_emi_table.search(loan_id=loan_id)
            for emi in emi_details:
                if 0 < emi['days_left'] < min_days:
                    count_valid_instances += 1
                    if count_valid_instances >= 2:
                        return True  # Two or more valid instances found, low risk
        return False  # Less than two valid instances found, not low risk

    def all_days_zero_2(self, loan_id):
        """Check if at least three instances of 'days_left' meet the condition and at least one instance falls between 0 and max_days"""
        lapsed_days = app_tables.fin_loan_settings.get(loans='lapsed fee')
        if lapsed_days:
            min_days = lapsed_days['minimum_days']
            max_days = lapsed_days['maximum_days']
            count_valid_instances = 0
            has_days_between_0_and_max = False
            
            emi_details = app_tables.fin_emi_table.search(loan_id=loan_id)
            for emi in emi_details:
                if 0 < emi['days_left'] < min_days:
                    count_valid_instances += 1
                if min_days <= emi['days_left'] <= max_days:
                    has_days_between_0_and_max = True
                # Check both conditions together
                if count_valid_instances >= 3 and has_days_between_0_and_max:
                    return True
            
            return False  # Condition not fully met: either less than three valid instances or no instance between 0 and max_days
        return False   

    def all_days_zero_3(self, loan_id):
        """Check if all 'days_left' for a given loan_id are greater than min_days"""
        lapsed_days = app_tables.fin_loan_settings.get(loans='lapsed fee')
        if lapsed_days:
            min_days = lapsed_days['minimum_days']
            emi_details = app_tables.fin_emi_table.search(loan_id=loan_id)
            for emi in emi_details:
                if emi['days_left'] <= min_days:
                    return False  # Found at least one instance where days_left is not greater than min_days
            return True  # All instances of days_left are greater than min_days
        return False 

    def initialize_plot(self):
        """Initialize the plot with aggregated counts"""
        fig = go.Figure(data=[
            go.Bar(name='No Risk', x=['No Risk'], y=[self.no_risk_count], marker_color='green', text=[f'{self.no_risk_count} Loans'], textposition='outside'),
            go.Bar(name='Low Risk', x=['Low Risk'], y=[self.low_risk_count], marker_color='yellow', text=[f'{self.low_risk_count} Loans'], textposition='outside'),
            go.Bar(name='Medium Risk', x=['Medium Risk'], y=[self.medium_risk_count], marker_color='orange', text=[f'{self.medium_risk_count} Loans'], textposition='outside'),
            go.Bar(name='High Risk', x=['High Risk'], y=[self.high_risk_count], marker_color='red', text=[f'{self.high_risk_count} Loans'], textposition='outside')
        ])

        fig.update_layout(
            title='Loan Risk Distribution',
            xaxis_title='Risk Level',
            yaxis_title='Number of Loans',
            barmode='group'
        )
        self.plot_4.figure = fig
      
    def show_loans(self, loans):
      """Method to show the loans list."""
      self.data_grid_1.visible = True
      self.display_loan_details(loans)  # Display loan details when showing loans
      self.risk_level_label.visible = True

    def hide_loans(self):
        """Method to hide the loans list."""
        self.data_grid_1.visible = False
        self.risk_level_label.visible = False
    
    def plot_4_click(self, points, **event_args):
        """This method is called when a data point is clicked."""
        if points:
            point = points[0]
            risk_level = point['x']
            
            if risk_level == 'No Risk':
                loans = self.no_risk_loans
            elif risk_level == 'Low Risk':
                loans = self.low_risk_loans
            elif risk_level == 'Medium Risk':
                loans = self.medium_risk_loans
            elif risk_level == 'High Risk':
                loans = self.high_risk_loans
            
            if self.selected_risk_level == risk_level:
                # If the same risk level is clicked again, hide the loans list
                self.hide_loans()
                self.selected_risk_level = None
            else:
                # If a different risk level is clicked, show the loans list
                self.show_loans(loans)
                self.selected_risk_level = risk_level


    def display_loan_details(self, loans):
        """Display loan details in the repeating panel"""
        self.repeating_panel_loan_details.items = loans

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.accounting')

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.dashboard.accounting.mis_reports.lender_share')

    def button_9_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.accounting.mis_reports.behavioural_report')

    def image_4_copy_copy_5_mouse_up(self, x, y, button, **event_args):
      """This method is called when a mouse button is released on this component"""
      open_form('admin.dashboard.accounting.mis_reports.behavioural_report')

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.convert_panel_to_pdf()

    def convert_panel_to_pdf(self):
      # Assuming 'content_panel' is the panel containing your data
      content_panel = self.content_panel
      
      # Call the server function to create the PDF from the content panel
      pdf = anvil.server.call('create_pdf_of_mis_reports', content_panel)
      
      # Prompt the user to download the PDF
      anvil.media.download(pdf)

    def eod_report_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.accounting.mis_reports.eod_reports')
