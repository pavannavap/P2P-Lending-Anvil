# from ._anvil_designer import manage_membershipTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class manage_membership(manage_membershipTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     # self.min_amount = 0

#     # Initially, check if there is any existing membership data
#     self.check_existing_membership_data()

#   def check_existing_membership_data(self):
#     # Define membership types
#     membership_types = ['Silver', 'Gold', 'Platinum']

#     for membership_type in membership_types:
#         row = app_tables.fin_membership.get(membership_type=membership_type)

#         if row is None:
#             self.enable_text_boxes(membership_type)
#             self.disable_edit_button(membership_type)
#         else:
#             self.populate_text_boxes(row, membership_type)
#             self.disable_text_boxes(membership_type)
#             self.enable_edit_button(membership_type)
#             self.disable_save_button(membership_type)


#   def populate_text_boxes(self, row, membership_type):
#     # Populate textboxes with existing data
#     if membership_type == 'Silver':
#       self.text_box_1.text = row['min_amount']
#       self.text_box_2.text = row['max_amount']
#     elif membership_type == 'Gold':
#       self.text_box_3.text = row['min_amount']
#       self.text_box_4.text = row['max_amount']
#     elif membership_type == 'Platinum':
#       self.text_box_5.text = row['min_amount']
#       self.text_box_6.text = row['max_amount']

#   def enable_text_boxes(self, membership_type):
#     # Enable textboxes for the specified membership type
#     #if membership_type == 'Silver':
#       self.text_box_1.enabled = True
#       self.text_box_2.enabled = True
#     #elif membership_type == 'Gold':
#       self.text_box_3.enabled = True
#       self.text_box_4.enabled = True
#     #elif membership_type == 'Platinum':
#       self.text_box_5.enabled = True
#       self.text_box_6.enabled = True

#   def disable_text_boxes(self, membership_type):
#     # Disable textboxes for the specified membership type
#     #if membership_type == 'Silver':
#       self.text_box_1.enabled = False
#       self.text_box_2.enabled = False
#     #elif membership_type == 'Gold':
#       self.text_box_3.enabled = False
#       self.text_box_4.enabled = False
#     #elif membership_type == 'Platinum':
#       self.text_box_5.enabled = False
#       self.text_box_6.enabled = False

#   def enable_edit_button(self, membership_type):
#     # Enable the corresponding edit button
#     if membership_type == 'Silver':
#       self.button_1.visible = True
#     elif membership_type == 'Gold':
#       self.button_1.visible = True
#     elif membership_type == 'Platinum':
#       self.button_1.visible = True

#   def disable_edit_button(self, membership_type):
#     # Disable the corresponding edit button
#     if membership_type == 'Silver':
#       self.button_1.visible = False
#     elif membership_type == 'Gold':
#       self.button_1.visible = False
#     elif membership_type == 'Platinum':
#       self.button_1.visible = False
      
#   def enable_save_button(self, membership_type):
#     # Enable the corresponding edit button
#     if membership_type == 'Silver':
#       self.button_2.visible = True
#     elif membership_type == 'Gold':
#       self.button_2.visible = True
#     elif membership_type == 'Platinum':
#       self.button_2.visible = True

#   def disable_save_button(self, membership_type):
#     # Disable the corresponding edit button
#     if membership_type == 'Silver':
#       self.button_2.visible = False
#     elif membership_type == 'Gold':
#       self.button_2.visible = False
#     elif membership_type == 'Platinum':
#       self.button_2.visible = False
  

#   def save_membership(self, membership_type):
#     print("Saving membership for:", membership_type)
#     # Determine which textboxes to read based on membership type
#     if membership_type == 'Silver':
#         min_amount = int(self.text_box_1.text)
#         max_amount = int(self.text_box_2.text)
#         if min_amount <= 0:
#             alert("Silver Minimum amount must be greater than zero!", title="Error")
#             return
#         if min_amount >= max_amount:
#             alert("Silver Minimum amount must be less than Silver maximum amount!", title="Error")
#             return
#         # Check if Silver's max_amount exceeds Gold's max_amount
#         gold_max = int(self.text_box_4.text)
#         if max_amount >= gold_max:
#             alert("Silver's max_amount cannot exceed Gold's max_amount or same!", title="Warning")
#             return
        
        
#     elif membership_type == 'Gold':
#         min_amount = int(self.text_box_3.text)
#         max_amount = int(self.text_box_4.text)
#         if min_amount <= 0:
#             alert("Gold Minimum amount can't be set as zero, it should be greater than Silver max-amount and less than Gold max_amount!", title="Error")
#             return
#         if min_amount >= max_amount:
#             alert("Gold Minimum amount must be less than Gold maximum amount!", title="Error")
#             return
#         silver_max = int(self.text_box_2.text)
#         if min_amount <= silver_max:
#             alert("Gold's min_amount must be greater than Silver's max_amount!", title="Error")
#             return
#         # Check if Gold's max_amount exceeds Platinum's max_amount
#         platinum_max = int(self.text_box_6.text)
#         if max_amount >= platinum_max:
#             alert("Gold's max_amount cannot exceed Platinum's max_amount or same!", title="Warning")
#             return
        
#     elif membership_type == 'Platinum':
#         min_amount = int(self.text_box_5.text)
#         max_amount = int(self.text_box_6.text)
#         if min_amount >= max_amount:
#             alert("Platinum Minimum amount must be less than Platinum maximum amount!", title="Error")
#             return
#         if min_amount <= 0:
#             alert("Platinum Minimum amount can't be set as zero, it should be greater than Gold max-amount and less than platinum max_amount!", title="Error")
#             return
#         gold_max = int(self.text_box_4.text)
#         if min_amount <= gold_max:
#             alert("platinum's min_amount must be greater than Silver's max_amount!", title="Error")
#             return
      
#     print("Min Amount:", min_amount)
#     print("Max Amount:", max_amount)

#     # Check if a row already exists for this membership type
#     existing_row = app_tables.fin_membership.get(membership_type=membership_type)
#     if existing_row is not None:
#         # Update the existing row with the provided min_amount and max_amount
#         existing_row.update(min_amount=min_amount, max_amount=max_amount)
#     else:
#         # If the row doesn't exist, create a new row with the provided min_amount and max_amount
#         app_tables.fin_membership.add_row(membership_type=membership_type, min_amount=min_amount, max_amount=max_amount)
      
#     if membership_type == 'Silver':
#         min_amount = int(self.text_box_1.text)
#         max_amount = int(self.text_box_2.text)
#         silver_row = app_tables.fin_membership.get(membership_type='Silver')
#         if min_amount >= max_amount:
#             alert("Minimum amount must be less than maximum amount!", title="Error")
#             return
#         # Check if Silver's max_amount exceeds Gold's min_amount
#         gold_row = app_tables.fin_membership.get(membership_type='Gold')
#         if gold_row is not None and gold_row['min_amount'] is not None and max_amount >= gold_row['min_amount']:
#             print("silver max", max_amount)
#             # gold_row['min_amount'] =  max_amount + 1
#             self.text_box_3.text = max_amount + 1  
#             alert("Silver's max_amount cannot exceed Gold's min_amount! Adjusting max_amount.", title="Warning")
       
#     elif membership_type == 'Gold':
#         min_amount = int(self.text_box_3.text)
#         max_amount = int(self.text_box_4.text)
#         if min_amount >= max_amount:
#             alert("Minimum amount must be less than maximum amount!", title="Error")
#             return
#         # Check if Gold's max_amount exceeds Platinum's min_amount
#         platinum_row = app_tables.fin_membership.get(membership_type='Platinum')
#         if platinum_row is not None and platinum_row['min_amount'] is not None and max_amount >= platinum_row['min_amount']:
#             self.text_box_5.text =  max_amount + 1
#             alert("Gold's max_amount cannot exceed Platinum's min_amount! Adjusting max_amount.", title="Warning")
        
#     elif membership_type == 'Platinum':
#         min_amount = int(self.text_box_5.text)
#         max_amount = int(self.text_box_6.text)
#         if min_amount >= max_amount:
#             alert("Minimum amount must be less than maximum amount!", title="Error")
#             return
#         # Ensure that Platinum's min_amount is greater than Gold's max_amount
#         gold_row = app_tables.fin_membership.get(membership_type='Gold')
#         if gold_row is not None and gold_row['max_amount'] is not None and min_amount <= gold_row['max_amount']:
#             min_amount = gold_row['max_amount'] + 1
#             alert("Platinum's min_amount cannot be less than or equal to Gold's max_amount! Adjusting min_amount.", title="Warning")

#     print("Min Amount:", min_amount)
#     print("Max Amount:", max_amount)
#     open_form('admin.dashboard.manage_settings.manage_membership')

#     # Re-enable edit and save buttons
#     self.disable_save_button(membership_type)
#     self.enable_edit_button(membership_type)
#     self.disable_text_boxes(membership_type)

#   def edit_membership(self, membership_type):
#     print("Editing membership for:", membership_type)
#     # Enable editing for the corresponding membership type
#     self.enable_text_boxes(membership_type)
#     # Disable the edit button
#     self.disable_edit_button(membership_type)
#     self.enable_save_button(membership_type)

#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     self.home_button_admin_1.visible = False
#     for membership_type in ['Silver', 'Gold', 'Platinum']:
#         self.edit_membership(membership_type)       

#   def button_2_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     for membership_type in ['Silver', 'Gold', 'Platinum']:
#         self.save_membership(membership_type)
#     open_form('admin.dashboard.manage_settings.manage_membership')

from ._anvil_designer import manage_membershipTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_membership(manage_membershipTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.min_amount = 0

    # Initially, check if there is any existing membership data
    self.check_existing_membership_data()

  def check_existing_membership_data(self):
    # Define membership types
    membership_types = ['Silver', 'Gold', 'Platinum']

    for membership_type in membership_types:
        row = app_tables.fin_membership.get(membership_type=membership_type)

        if row is None:
            self.enable_text_boxes(membership_type)
            self.disable_edit_button(membership_type)
        else:
            self.populate_text_boxes(row, membership_type)
            self.disable_text_boxes(membership_type)
            self.enable_edit_button(membership_type)
            self.disable_save_button(membership_type)


  def populate_text_boxes(self, row, membership_type):
    # Populate textboxes with existing data
    if membership_type == 'Silver':
      self.text_box_1.text = row['min_amount']
      self.text_box_2.text = row['max_amount']
    elif membership_type == 'Gold':
      self.text_box_3.text = row['min_amount']
      self.text_box_4.text = row['max_amount']
    elif membership_type == 'Platinum':
      self.text_box_5.text = row['min_amount']
      self.text_box_6.text = row['max_amount']

  def enable_text_boxes(self, membership_type):
    # Enable textboxes for the specified membership type
    #if membership_type == 'Silver':
      self.text_box_1.enabled = True
      self.text_box_2.enabled = True
    #elif membership_type == 'Gold':
      self.text_box_3.enabled = True
      self.text_box_4.enabled = True
    #elif membership_type == 'Platinum':
      self.text_box_5.enabled = True
      self.text_box_6.enabled = True

  def disable_text_boxes(self, membership_type):
    # Disable textboxes for the specified membership type
    #if membership_type == 'Silver':
      self.text_box_1.enabled = False
      self.text_box_2.enabled = False
    #elif membership_type == 'Gold':
      self.text_box_3.enabled = False
      self.text_box_4.enabled = False
    #elif membership_type == 'Platinum':
      self.text_box_5.enabled = False
      self.text_box_6.enabled = False

  def enable_edit_button(self, membership_type):
    # Enable the corresponding edit button
    if membership_type == 'Silver':
      self.button_1.visible = True
    elif membership_type == 'Gold':
      self.button_1.visible = True
    elif membership_type == 'Platinum':
      self.button_1.visible = True

  def disable_edit_button(self, membership_type):
    # Disable the corresponding edit button
    if membership_type == 'Silver':
      self.button_1.visible = False
    elif membership_type == 'Gold':
      self.button_1.visible = False
    elif membership_type == 'Platinum':
      self.button_1.visible = False
      
  def enable_save_button(self, membership_type):
    # Enable the corresponding edit button
    if membership_type == 'Silver':
      self.button_2.visible = True
    elif membership_type == 'Gold':
      self.button_2.visible = True
    elif membership_type == 'Platinum':
      self.button_2.visible = True

  def disable_save_button(self, membership_type):
    # Disable the corresponding edit button
    if membership_type == 'Silver':
      self.button_2.visible = False
    elif membership_type == 'Gold':
      self.button_2.visible = False
    elif membership_type == 'Platinum':
      self.button_2.visible = False
  

  def save_membership(self, membership_type):
    print("Saving membership for:", membership_type)
    # Determine which textboxes to read based on membership type
    if membership_type == 'Silver':
        min_amount = int(self.text_box_1.text)
        max_amount = int(self.text_box_2.text)
        if min_amount <= 0:
            alert("Silver Minimum amount must be greater than zero!", title="Error")
            return
        if min_amount >= max_amount:
            alert("Silver Minimum amount must be less than Silver maximum amount!", title="Error")
            return
        # Check if Silver's max_amount exceeds Gold's max_amount
        gold_max = int(self.text_box_4.text)
        if max_amount >= gold_max:
            alert("Silver's max_amount cannot exceed Gold's max_amount or same!", title="Warning")
            return
        
        
    elif membership_type == 'Gold':
        min_amount = int(self.text_box_3.text)
        max_amount = int(self.text_box_4.text)
        if min_amount <= 0:
            alert("Gold Minimum amount can't be set as zero, it should be greater than Silver max-amount and less than Gold max_amount!", title="Error")
            return
        if min_amount >= max_amount:
            alert("Gold Minimum amount must be less than Gold maximum amount!", title="Error")
            return
        silver_max = int(self.text_box_2.text)
        if min_amount <= silver_max:
            alert("Gold's min_amount must be greater than Silver's max_amount!", title="Error")
            return
        # Check if Gold's max_amount exceeds Platinum's max_amount
        platinum_max = int(self.text_box_6.text)
        if max_amount >= platinum_max:
            alert("Gold's max_amount cannot exceed Platinum's max_amount or same!", title="Warning")
            return
        
    elif membership_type == 'Platinum':
        min_amount = int(self.text_box_5.text)
        max_amount = int(self.text_box_6.text)
        if min_amount >= max_amount:
            alert("Platinum Minimum amount must be less than Platinum maximum amount!", title="Error")
            return
        if min_amount <= 0:
            alert("Platinum Minimum amount can't be set as zero, it should be greater than Gold max-amount and less than platinum max_amount!", title="Error")
            return
        gold_max = int(self.text_box_4.text)
        if min_amount <= gold_max:
            alert("platinum's min_amount must be greater than Gold's max_amount!", title="Error")
            return
      
    print("Min Amount:", min_amount)
    print("Max Amount:", max_amount)

    # Check if a row already exists for this membership type
    existing_row = app_tables.fin_membership.get(membership_type=membership_type)
    if existing_row is not None:
        # Update the existing row with the provided min_amount and max_amount
        existing_row.update(min_amount=min_amount, max_amount=max_amount)
    else:
        # If the row doesn't exist, create a new row with the provided min_amount and max_amount
        app_tables.fin_membership.add_row(membership_type=membership_type, min_amount=min_amount, max_amount=max_amount)
      
    if membership_type == 'Silver':
        min_amount = int(self.text_box_1.text)
        max_amount = int(self.text_box_2.text)
        silver_row = app_tables.fin_membership.get(membership_type='Silver')
        if min_amount >= max_amount:
            alert("Minimum amount must be less than maximum amount!", title="Error")
            return
        # Check if Silver's max_amount exceeds Gold's min_amount
        gold_row = app_tables.fin_membership.get(membership_type='Gold')
        if gold_row is not None and gold_row['min_amount'] is not None and max_amount >= gold_row['min_amount']:
            print("silver max", max_amount)
            # gold_row['min_amount'] =  max_amount + 1
            self.text_box_3.text = max_amount + 1  
            alert("Silver's max_amount cannot exceed Gold's min_amount! Adjusting max_amount.", title="Warning")
       
    elif membership_type == 'Gold':
        min_amount = int(self.text_box_3.text)
        max_amount = int(self.text_box_4.text)
        if min_amount >= max_amount:
            alert("Minimum amount must be less than maximum amount!", title="Error")
            return
        # Check if Gold's max_amount exceeds Platinum's min_amount
        platinum_row = app_tables.fin_membership.get(membership_type='Platinum')
        if platinum_row is not None and platinum_row['min_amount'] is not None and max_amount >= platinum_row['min_amount']:
            self.text_box_5.text =  max_amount + 1
            alert("Gold's max_amount cannot exceed Platinum's min_amount! Adjusting max_amount.", title="Warning")
        
    elif membership_type == 'Platinum':
        min_amount = int(self.text_box_5.text)
        max_amount = int(self.text_box_6.text)
        if min_amount >= max_amount:
            alert("Minimum amount must be less than maximum amount!", title="Error")
            return
        # Ensure that Platinum's min_amount is greater than Gold's max_amount
        gold_row = app_tables.fin_membership.get(membership_type='Gold')
        if gold_row is not None and gold_row['max_amount'] is not None and min_amount <= gold_row['max_amount']:
            min_amount = gold_row['max_amount'] + 1
            alert("Platinum's min_amount cannot be less than or equal to Gold's max_amount! Adjusting min_amount.", title="Warning")

    print("Min Amount:", min_amount)
    print("Max Amount:", max_amount)
    open_form('admin.dashboard.manage_settings.manage_membership')

    # Re-enable edit and save buttons
    self.disable_save_button(membership_type)
    self.enable_edit_button(membership_type)
    self.disable_text_boxes(membership_type)

  def edit_membership(self, membership_type):
    print("Editing membership for:", membership_type)
    # Enable editing for the corresponding membership type
    self.enable_text_boxes(membership_type)
    # Disable the edit button
    self.disable_edit_button(membership_type)
    self.enable_save_button(membership_type)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.home_button_admin_1.visible = False
    for membership_type in ['Silver', 'Gold', 'Platinum']:
        self.edit_membership(membership_type)       

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    for membership_type in ['Silver', 'Gold', 'Platinum']:
        self.save_membership(membership_type)
    open_form('admin.dashboard.manage_settings.manage_membership')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings')
