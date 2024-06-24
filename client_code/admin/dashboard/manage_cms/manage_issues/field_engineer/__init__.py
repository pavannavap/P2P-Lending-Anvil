from ._anvil_designer import field_engineerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.http
import math
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class field_engineer(field_engineerTemplate):
  def __init__(self, selected_row, **properties):
    self.init_components(**properties)

    self.selected_row = selected_row
    self.id = selected_row['customer_id']
    self.label_17.text = self.id

    self.user_profile = app_tables.fin_user_profile.get(customer_id=self.id)
    self.label_6.text = self.user_profile['street_adress_1']
    customer_details = app_tables.fin_reported_problems.get(customer_id=self.id)
    self.image_1.source = customer_details['user_photo']
    self.label_2.text = customer_details['name']
    self.label_4.text = customer_details['mobile_number']
    self.label_8.text = customer_details['category']
    self.label_10.text = customer_details['subcategory']
    self.label_13.text = customer_details['issue_description']
    self.label_14.text = customer_details['usertype']
    self.address = self.user_profile['street_adress_1']
    self.category = customer_details['category']
    self.selected_engineer = None
    if self.category == 'Lone Issue':
      self.find_nearest_field_engineer()
      self.save_button()
    else:
      self.label_18.text = 'This Issue Checked By Technical Team'

  def get_coordinates(self, address):
    # Call Nominatim API to get coordinates
    response = anvil.http.request(
        f"https://nominatim.openstreetmap.org/search?format=json&q={address}",
        method="GET",
        json=True  # Ensures the response is parsed as JSON
    )
    if response:
        location = response[0]
        print(f"Address: {address}, Coordinates: ({location['lat']}, {location['lon']})")
        return (float(location['lat']), float(location['lon']))
    else:
        print(f"Address: {address}, Coordinates: Not Found")
        return (0, 0)  # Default to (0, 0) if no results found

  def calculate_distance(self, coord1, coord2):
    # Function to calculate distance between two coordinates using Haversine formula
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Haversine formula
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    rounded_distance = round(distance)

    print(f"Distance between {coord1} and {coord2}: {rounded_distance} km")
    return rounded_distance

  def find_nearest_field_engineer(self):
    customer_address = self.user_profile['street_adress_1']
    customer_coordinates = self.get_coordinates(customer_address)

    field_engineers = app_tables.fin_field_engineers.search()
    distances = []

    for engineer in field_engineers:
      engineer_address = engineer['address']
      engineer_coordinates = self.get_coordinates(engineer_address)

      distance = self.calculate_distance(customer_coordinates, engineer_coordinates)
      distances.append((distance, engineer))

    # Sort field engineers by distance
    distances.sort(key=lambda x: x[0])

    # Populate dropdown with sorted field engineers
    self.drop_down_1.items = [
      f"{engineer['full_name']} ({distance} km)" for distance, engineer in distances
    ]

    # Select the nearest engineer
    if distances:
      nearest_engineer = distances[0][1]
      print(f"Nearest Engineer: {nearest_engineer['full_name']}, Distance: {distances[0][0]} km")
      self.selected_engineer = nearest_engineer

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.manage_issues')

  def save_button(self, **event_args):
    self.column_panel_2.visible = True

  def button_2_click(self, **event_args):
    print(self.label_18.text)
    update = self.label_18.text.strip()
    self.selected_row['field_engineer'] = update
    self.selected_row.update()
    alert("Issue Assigned")
    open_form('admin.dashboard.manage_cms.manage_issues')
