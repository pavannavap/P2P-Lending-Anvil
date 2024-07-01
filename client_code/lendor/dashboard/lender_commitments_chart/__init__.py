from ._anvil_designer import lender_commitments_chartTemplate
from anvil import *
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
import plotly.graph_objects as go
import anvil.media


class lender_commitments_chart(lender_commitments_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)   
    self.email = main_form_module.email
    print(self.email)
    self.id = main_form_module.userId
    self.create_bar_chart()

    def create_pie_chart(self, data):
    labels = list(data.keys())
    values = list(data.values())
    
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, 
                                 textinfo='label+percent', insidetextorientation='radial', hole=.3)])
    
    fig.update_layout(title_text='Lender Commitments')
    
    # Bind the plotly figure to the Plot component
    self.plot_1.figure = fig