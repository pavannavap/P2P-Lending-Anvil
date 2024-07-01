from ._anvil_designer import view_transaction_historyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module


class view_transaction_history(view_transaction_historyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId
        print(self.user_id)
        
        # Fetch transaction data based on customer_id and transaction_type
        self.result = []
        transactions_received = app_tables.fin_wallet_transactions.search(
            customer_id=self.user_id,
            transaction_type = 'transferred to'
        )
        transactions_transferred = app_tables.fin_wallet_transactions.search(
            receiver_customer_id=self.user_id,
            transaction_type = 'received from'
        )
        
        for transaction_data in transactions_received:
            lender_profile = app_tables.fin_user_profile.get(email_user=transaction_data['user_email'])
            borrower_profile = app_tables.fin_user_profile.get(customer_id=transaction_data['receiver_customer_id'])
            if borrower_profile is not None and lender_profile is not None:
                self.result.append({
                    'borrower_full_name': borrower_profile['full_name'],                    
                    'lender_full_name': lender_profile['full_name'],
                    'amount': "{:.2f}".format(transaction_data['amount']),
                    'transaction_time_stamp': transaction_data['transaction_time_stamp'],
                    'user_email': transaction_data['user_email'],
                    'status': transaction_data['status'],
                    # 'transaction_time_stamp': transaction_data['transaction_time_stamp'],
                    'transaction_id': transaction_data['transaction_id'],
                    'transaction_type': transaction_data['transaction_type'],
                    'borrower_mobile': borrower_profile['mobile'], 
                    'lender_mobile': lender_profile['mobile']  ,
                    'wallet_id': transaction_data['wallet_id'],
                    'receiver_email': transaction_data['receiver_email'],
                    # 'transaction_id': transaction_data['transaction_id'],
                })
        
        for transaction_data in transactions_transferred:
            lender_profile = app_tables.fin_user_profile.get(email_user=transaction_data['user_email'])
            borrower_profile = app_tables.fin_user_profile.get(customer_id=transaction_data['receiver_customer_id'])
            if borrower_profile is not None and lender_profile is not None:
                self.result.append({
                    'borrower_full_name': borrower_profile['full_name'],                    
                    'lender_full_name': lender_profile['full_name'],
                    'amount': "{:.2f}".format(transaction_data['amount']),
                    'transaction_time_stamp': transaction_data['transaction_time_stamp'],
                    'user_email': transaction_data['user_email'],
                    'status': transaction_data['status'],
                    # 'transaction_time_stamp': transaction_data['transaction_time_stamp'],
                    'transaction_id': transaction_data['transaction_id'],
                    'transaction_type': transaction_data['transaction_type'],
                    'borrower_mobile': borrower_profile['mobile'], 
                    'lender_mobile': lender_profile['mobile']  ,
                    'wallet_id': transaction_data['wallet_id'],
                    'receiver_email': transaction_data['receiver_email'],
                })

        self.repeating_panel_2.items = self.result

 