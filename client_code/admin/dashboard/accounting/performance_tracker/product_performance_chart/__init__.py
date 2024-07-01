from ._anvil_designer import product_performance_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class product_performance_chart(product_performance_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
    # Fetch all products
    self.data = tables.app_tables.fin_product_details.search()
    product_name_count = len([record for record in self.data if record['product_name']])
    self.label_2.text = str(product_name_count)
    # Fetch All loan deatails
    self.data = app_tables.fin_loan_details.search()
    
    # Process the data to get the count of loans per product name
    product_counts = {}
    for row in self.data:
      product_name = row['product_name']
      if product_name in product_counts:
        product_counts[product_name] += 1
      else:
        product_counts[product_name] = 1

    # Create the pie chart
    # fig = go.Figure(data=[go.Pie(labels=list(product_counts.keys()), values=list(product_counts.values()))])
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=list(product_counts.keys()), 
                                     values=list(product_counts.values()),
                                     textinfo='label+value',)])  # Display only the label
    # Set chart title
    fig.update_layout(title_text='Product Performance of Perticular Product')

    # Add the chart to the form
    self.plot_1.figure = fig

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.accounting.performance_tracker')
