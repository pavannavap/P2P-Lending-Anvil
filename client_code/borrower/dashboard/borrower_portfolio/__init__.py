from ._anvil_designer import borrower_portfolioTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....bank_users.main_form import main_form_module
from ....bank_users.user_form import user_form
from ....bank_users.user_form import user_module
import datetime
import anvil.media
# from kivy.utils import get_color_from_hex

class borrower_portfolio(borrower_portfolioTemplate):
  def __init__(self, selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_row=selected_row
    self.id= selected_row['customer_id']
    # self.email = main_form_module.email
    # print(self.email)
    # self.id = main_form_module.userId
    self.create_bar_chart()

    # Set the label text with today's date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    self.label_2.text = "As on " + today_date


    # Retrieve user profile based on user_Id
    ascend = app_tables.fin_user_profile.get(customer_id=self.id)
    self.image_4.source = ascend['user_photo']
    self.label_4.text = "Hello" " " + ascend['full_name']
    self.name = ascend['full_name']
    self.label_15.text = ascend['mobile']
    self.label_16.text = ascend['date_of_birth']
    self.label_17.text = ascend['gender']
    self.label_18.text = ascend['marital_status']
    self.label_19.text = ascend['present_address']
    self.label_20.text = ascend['qualification']
    self.label_21.text = ascend['profession']
    if ascend['profession'].lower() in ("employee", "self employment"):
        self.label_22.visible = True
        self.label_14.visible = True
        self.label_22.text = ascend['annual_salary']
    
    
    # Check if the profile exists and the ascend value is valid
    if ascend:
        ascend_value = ascend['ascend_value']
        
        # Ensure ascend_value is a number
        if isinstance(ascend_value, (int, float)):
            # Set the label text to the ascend value
            self.ascend_score_label.text = str(ascend_value)
            
            # Update background color based on score range
            # Fetch all score ranges from the table
            score_ranges = app_tables.fin_ascend_score_range.search()
            
            # Initialize default values
            background_color = "#FFFFFF"  # Default to white
            ascend_category = "Unknown"   # Default category
            
            # Iterate through the score ranges to find the correct background color and category
            for score_range in score_ranges:
                min_range = score_range['min_ascend_score_range']
                max_range = score_range['max_ascend_score_range']
                color = score_range['color'] 
                category = score_range['ascend_category']  
            
                if min_range <= ascend_value <= max_range:
                    background_color = color
                    ascend_category = category
                    break
            
            # Update the background color and display the category
            self.ascend_score_label.background = background_color
            self.ascend_score_label.text = ascend_category           
        else:
            print("Ascend value is not a number.")
    else:
        print("No profile found or 'ascend_value' not in profile.")



    rows = app_tables.fin_loan_details.search(borrower_customer_id=self.id, loan_updated_status=q.any_of(
          q.like('accepted%'),          
          q.like('approved%'),
          q.like('foreclosure%'),
          q.like('disbursed%'),          
        ))
    self.label_5_copy.text = len(rows)
    
    row = app_tables.fin_loan_details.search(borrower_customer_id=self.id, loan_updated_status=q.any_of(
          q.like('closed%')
        ))
    self.label_9.text = len(row)
    
    no_of_disbursed_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.id, loan_updated_status=q.any_of(
          q.like('disbursed%')          
        ))
    self.label_3_copy.text = len(no_of_disbursed_loans)

    amount_of_disbursed_loans = app_tables.fin_loan_details.search(
    borrower_customer_id=self.id,
    loan_updated_status="disbursed"
)

    if amount_of_disbursed_loans:
        # Calculate total loan amount
        total_amount = sum(loan['loan_amount'] for loan in amount_of_disbursed_loans)
        self.label_9_copy.text=total_amount
        print("Total disbursed loan amount:", total_amount)
    else:
        print("No disbursed loans found for this borrower.")

      
    # Fetch the loan status data for the given customer_id
    loan_status_data = self.get_loan_status_data(self.id)
    
    # Create the pie chart with the fetched data
    self.create_pie_chart(loan_status_data)
    
  def get_loan_status_data(self, borrower_customer_id):
    # Query the database to get loan status data for the given customer_id
    rows = app_tables.fin_loan_details.search(borrower_customer_id=borrower_customer_id)
    loan_status_counts = {}
    
    # Count the occurrences of each loan status
    for row in rows:
        status = row['loan_updated_status']
        if status in loan_status_counts:
            loan_status_counts[status] += 1
        else:
            loan_status_counts[status] = 1
            
    return loan_status_counts

  def create_pie_chart(self, data):
    labels = list(data.keys())
    values = list(data.values())
    
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, 
                                 textinfo='label+percent', insidetextorientation='radial', hole=.3)])
    
    fig.update_layout(title_text='Loans Distribution')
    
    # Bind the plotly figure to the Plot component
    self.plot_1.figure = fig


  def create_bar_chart(self):
        # Fetch data from the table
        score_ranges = app_tables.fin_ascend_score_range.search()

        # Prepare data for the bar chart
        categories = []
        min_ranges = []
        max_ranges = []

        for score_range in score_ranges:
            categories.append(score_range['ascend_category'])
            min_ranges.append(score_range['min_ascend_score_range'])
            max_ranges.append(score_range['max_ascend_score_range'])


        # Create a trace for max_range
        max_trace = go.Bar(
            x=categories,
            y=max_ranges,
            name='Max Range',
            marker=dict(color='#00FF00')  # Green for max range
        )
    
        # Create a trace for min_range
        min_trace = go.Bar(
            x=categories,
            y=min_ranges,
            name='Min Range',
            marker=dict(color='#FFA500')  # Orange for min range
        )

        # Create the figure with both traces
        fig = go.Figure(data=[max_trace, min_trace])

        # Set chart title and labels
        fig.update_layout(
            title='Ascend Score Ranges by Category',
            xaxis_title='Ascend Category',
            yaxis_title='Range Value',
            barmode='group'  
        )

        # Display the chart in an Anvil component
        self.plot_2.figure = fig
     

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.convert_panel_to_pdf()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard')

  def convert_panel_to_pdf(self):
      # Assuming 'content_panel' is the panel containing your data
      content_panel = self.content
      
      # Call the server function to create the PDF from the content panel
      pdf = anvil.server.call('create_pdf_of_borrower_portfolio', content_panel)
      
      # Prompt the user to download the PDF
      anvil.media.download(pdf)