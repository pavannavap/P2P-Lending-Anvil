from ._anvil_designer import key_metriceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class key_metrice(key_metriceTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.repeating_panel_1.items = []
        self.all_items = []

        # Aggregate counts for all risk levels and initialize plot
        self.aggregate_counts()
        self.initialize_plot()
        self.set_button_colors()

    def set_button_colors(self):
        """Set the colors of the buttons based on the respective risk levels"""
        risk_level_to_button = {
            'VeryGood': self.button_1_copy,
            'Good': self.button_2_copy,
            'Average': self.button_5_copy,
            'Bad': self.button_1_copy_copy
        }

        for risk_level, button in risk_level_to_button.items():
            filtered_rows, color = self.get_filtered_rows(risk_level)
            button.background = color if color else '#FFFFFF'  # Set default color if color is None

    def aggregate_counts(self):
        """Aggregate the counts of loans for each risk level"""
        categories = ['VeryGood', 'Good', 'Average', 'Bad']
        for category in categories:
            filtered_rows, _ = self.get_filtered_rows(category)
            setattr(self, f"{category.lower()}_count", len(filtered_rows))

    def get_filtered_rows(self, risk_level):
        """Fetch and filter rows from EMI table based on risk level"""
        lapsed_settings = app_tables.fin_ascend_score_range.get(ascend_category=risk_level)
        if not lapsed_settings:
            print(f"No settings found for risk level: {risk_level}")
            return [], None

        min_days = lapsed_settings['min_ascend_score_range']
        max_days = lapsed_settings['max_ascend_score_range']
        color = lapsed_settings['color']

        emi_rows = app_tables.fin_borrower.search()
        if emi_rows is None:
            print("Failed to fetch rows from fin_borrower table")
            return [], None

        filtered_rows = [row for row in emi_rows if min_days <= row['ascend_score'] <= max_days]
        return filtered_rows, color

    def initialize_plot(self):
        """Initialize the plot with aggregated counts and dynamically fetched colors"""
        categories = ['VeryGood', 'Good', 'Average', 'Bad']
        bars = []
        colors = []
        for category in categories:
            # Fetch color from the fin_ascend_score_range table
            filtered_rows, color = self.get_filtered_rows(category)
            # Aggregate count
            count = getattr(self, f"{category.lower()}_count", 0)
            bars.append(go.Bar(name=category, x=[category], y=[count]))
            colors.append(color if color else '#FFFFFF')  # Set default color if color is None

        fig = go.Figure(data=bars)

        fig.update_layout(title='Key Metrics Analysis',
                          xaxis={'title': 'Ascend Categories'},
                          yaxis={'title': 'Number of Borrower'},
                          barmode='group')

        # Assigning colors to bars
        for i in range(len(fig.data)):
            fig.data[i].marker.color = colors[i]

        self.risk_plot.data = fig.data
        self.risk_plot.layout = fig.layout

    def very_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_panel("VeryGood")
        # self.update_plot()

    def good_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_panel("Good")
        # self.update_plot()

    def average_clik(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_panel("Average")
        # self.update_plot()

    def bad_clidk(self, **event_args):
        """This method is called when the button is clicked"""
        self.update_panel("Bad")
        # self.update_plot()

    def update_panel(self, risk_level):
        """Update the panel with filtered rows"""
        filtered_rows, color = self.get_filtered_rows(risk_level)
        result = []
        for row in filtered_rows:
            user_details = app_tables.fin_user_profile.get(customer_id=row['customer_id'])
            if user_details:
                combined_data = {
                    'customer_id': row['customer_id'],
                    'borrower_since': row['borrower_since'],
                    'user_name': row['user_name'],
                    'ascend_score': row['ascend_score'],
                    'email_id': row['email_id'],
                    'credit_limit': row['credit_limit'],
                    'mobile': user_details['mobile'],
                }
                result.append(combined_data)
        self.all_items = result
        self.repeating_panel_1.items = result
        self.text_box_search.placeholder = f'Search {risk_level} Ascend Score'
        self.label.visible = True
        self.label.text = f'{risk_level} Ascend Score details'
        self.data_grid_1.visible = True
        self.column_panel_1.visible = True
        self.data_grid_2.visible = False

    def update_plot(self):
        """Update the plot with aggregated counts"""
        self.aggregate_counts()
        self.initialize_plot()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.reporting_and_analytical_modules')
