from ._anvil_designer import application_intakeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from collections import defaultdict

class application_intake(application_intakeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.update_loan_status_count()
        self.display_loan_status_graph()

    def update_loan_status_count(self):
        # Fetch all loan records from the fin_loan_details table
        loans = app_tables.fin_loan_details.search()
        
        # Initialize counters
        total_count = 0
        disbursed_count = 0
        rejected_count = 0
        
        # Count the statuses
        for loan in loans:
            status = loan['loan_updated_status']
            if status is not None:
                total_count += 1
                if status == 'approved':
                    disbursed_count += 1
                elif status == 'rejected':
                    rejected_count += 1
        
        # Update the labels with the counts
        self.label_1.text = f"{total_count}"
        self.label_3.text = f"{disbursed_count}"
        self.label_4.text = f"{rejected_count}"

    def date_picker_1_change(self, **event_args):
        selected_date = self.date_picker_1.date  # Use .date to get the selected date
        
        if selected_date:
            # Filter loans for the selected date
            loans_for_date = [loan for loan in app_tables.fin_loan_details.search()
                              if loan['borrower_loan_created_timestamp'] == selected_date]
            
            if loans_for_date:
                # If there are loans for the selected date, update the graph
                self.display_loan_status_graph(time_period='date', loans=loans_for_date, selected_date=selected_date)
            else:
                # If no loans found, show an alert
                alert('the selected date date doesnt have any value', 'There are no loans for the selected date.', 'OK')
        else:
            alert('No date selected', 'Please select a date to view loan status.', 'OK')

    def display_loan_status_graph(self, time_period='month', loans=None, selected_date=None):
        if loans is None:
            loans = app_tables.fin_loan_details.search()
    
        # Initialize a dictionary to count statuses by the selected time period
        loan_counts_by_period = defaultdict(lambda: {'approved': 0, 'rejected': 0})
    
        # Count all values in loan_updated_status
        total_status_count = 0
        for loan in loans:
            status = loan['loan_updated_status']
            if status is not None:
                total_status_count += 1
    
        # Initialize the graph_title with a default value
        graph_title = 'Loan Status Count'
    
        # Count statuses by the specified time period
        for loan in loans:
            status = loan['loan_updated_status']
            loan_date = loan['borrower_loan_created_timestamp']  # Assuming this is the correct timestamp field
    
            if time_period == 'date' and selected_date:
                # Handle date-specific logic
                loan_created_date = loan_date  # No need for .date() conversion
                if loan_created_date == selected_date:
                    period = selected_date.strftime('%d-%m-%Y')
                    graph_title = 'Loan Status Count for Selected Date'
                    if status == 'approved':
                        loan_counts_by_period[period]['approved'] += 1
                    elif status == 'rejected':
                        loan_counts_by_period[period]['rejected'] += 1
            elif time_period == 'year':
                period = loan_date.strftime('%Y')
                graph_title = 'Loan Status Count by Year'
                if status == 'approved':
                    loan_counts_by_period[period]['approved'] += 1
                elif status == 'rejected':
                    loan_counts_by_period[period]['rejected'] += 1
            else:  # Default to 'month'
                period = loan_date.strftime('%m-%y')
                graph_title = 'Loan Status Count by Month'
                if status == 'approved':
                    loan_counts_by_period[period]['approved'] += 1
                elif status == 'rejected':
                    loan_counts_by_period[period]['rejected'] += 1
    
        # Prepare data for the bar graph
        periods = sorted(loan_counts_by_period.keys())
        approved_counts = [loan_counts_by_period[period]['approved'] for period in periods]
        rejected_counts = [loan_counts_by_period[period]['rejected'] for period in periods]
    
        # Create a bar graph with adjusted width and spacing
        fig = go.Figure(data=[
            go.Bar(name='Approved', x=periods, y=approved_counts, marker_color='green', width=0.1),
            go.Bar(name='Rejected', x=periods, y=rejected_counts, marker_color='red', width=0.1)
        ])
    
        # Update the layout of the graph
        fig.update_layout(
            title=graph_title,
            xaxis_title='Time Period',
            yaxis_title='Total Loan Count',
            barmode='group',
            bargap=0.75,  # Gap between bars of adjacent location coordinates
            bargroupgap=0.7,  # Gap between bars of the same location coordinates
            xaxis=dict(
                tickmode='array' if time_period == 'year' else 'linear',
                tickvals=periods if time_period == 'year' else None,
                ticktext=periods if time_period == 'year' else None
            ),
            yaxis=dict(
                title='Total Loan Count',
                range=[0, total_status_count ]  # Adjusted range to ensure proper visualization
            )
        )
    
        # Display the graph in the Plot component
        self.plot_1.figure = fig

    def month_button_click_click(self, **event_args):
        """This method is called when the Month button is clicked"""
        self.display_loan_status_graph(time_period='month')
        
    def year_button_click_click(self, **event_args):
        """This method is called when the Year button is clicked"""
        self.display_loan_status_graph(time_period='year')        

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.loan_management')

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.loan_management.application_intake.All_loans')

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.loan_management.application_intake.Approved_loans')

    def button_5_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.loan_management.application_intake.Rejected_loans')

    def image_1_mouse_up(self, x, y, button, **event_args):
        """This method is called when a mouse button is released on this component"""
        open_form('admin.dashboard.loan_management.application_intake.All_loans')

    def image_1_copy_3_mouse_up(self, x, y, button, **event_args):
        """This method is called when a mouse button is released on this component"""
        open_form('admin.dashboard.loan_management.application_intake.Approved_loans')

    def image_1_copy_mouse_up(self, x, y, button, **event_args):
        """This method is called when a mouse button is released on this component"""
        open_form('admin.dashboard.loan_management.application_intake.Rejected_loans')

    

    



    

