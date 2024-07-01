import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
import anvil.media
# from weasyprint import HTML

# all emi receipt
@anvil.server.callable
def create_pdf_from_panel(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.render_form(content_panel)
    
    return pdf

# each emi receipt
@anvil.server.callable
def create_pdf_of_payment_receipt(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4', scale = 0.85).render_form(content_panel)
    
    return pdf

# code to generate pdf of borrower portfolio
@anvil.server.callable
def create_pdf_of_borrower_portfolio(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4').render_form(content_panel)
    
    return pdf

# code to generate pdf of lender portfolio
@anvil.server.callable
def create_pdf_of_lender_portfolio(content_panel):
    # Render the panel to a PDF
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4').render_form(content_panel)
    
    return pdf
  

# code to generate pdf of MIS reports
@anvil.server.callable
def create_pdf_of_mis_reports(content_panel):
    # Render the panel to a PDF
    custom_page_size = (28, 35)
    pdf = anvil.pdf.PDFRenderer(landscape=True, page_size='A4', scale = 0.85, quality='screen').render_form(content_panel)
    
    return pdf
  
# @anvil.server.callable
# def create_pdf(name, image_source,selected_row):    
#     # Your PDF creation logic here
#     pdf = anvil.pdf.PDFRenderer(landscape=True).render_form("lendor.dashboard.lender_portfolio",selected_row = selected_row)  
#     return pdf
     
# @anvil.server.callable()
# def create_pdf1(name, image_source, selected_row):
#     # A4 size in points (width, height) is (595, 842), for landscape swap to (842, 595)
#     # landscape_a4 = (842, 595)   
#     # Create the PDF in landscape mode by specifying the size
#     pdf = anvil.pdf.PDFRenderer(landscape=True).render_form("borrower.dashboard.borrower_portfolio", selected_row=selected_row)   
#     return pdf


# @anvil.server.callable()
# def create_pdf1(name, image_source, selected_row):
    
#     # Your PDF creation logic here
#     pdf = anvil.pdf.PDFRenderer(page_size='A4', orientation='landscape').render_form("borrower.dashboard.borrower_portfolio", selected_row=selected_row)  
#     return pdf


# @anvil.server.background_task
# def create_pdf_background(name, image_source, selected_row):
#     landscape_a4 = (842, 595)
#     pdf = anvil.pdf.PDFRenderer(page_size=landscape_a4).render_form("lendor.dashboard.lender_portfolio", selected_row=selected_row)
#     return pdf


# @anvil.server.callable
# def start_create_pdf_background(name, image_source, selected_row):
#     task = anvil.server.launch_background_task('create_pdf_background', name, image_source, selected_row)
#     return task.get_id()

# @anvil.server.background_task
# def create_pdf_background(name, image_source, selected_row):
#     landscape_a4 = (842, 595)
#     pdf = anvil.pdf.PDFRenderer(page_size=landscape_a4).render_form("lendor.dashboard.lender_portfolio", selected_row=selected_row)
#     return pdf

# @anvil.server.callable
# def get_task_status(task_id):
#     task = anvil.server.get_background_task(task_id)
#     if task:
#         state = task.get_state()
#         return {
#             'status': state.get('status', 'unknown'),
#             'result': state.get('return_value', None),
#             'error': state.get('error', None)
#         }
#     else:
#         return {'status': 'unknown', 'result': None, 'error': 'Task not found'}


