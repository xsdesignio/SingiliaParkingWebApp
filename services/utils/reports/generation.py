from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import Table

from datetime import datetime
from services.users.entities.user import User
from services.zones.entities.zone import Zone



# Create function that create a report with the data of the tickets printed by a certain user over a pdf file saved on the server in the reports folder from static.
def create_report(data: dict, user: User, start_date: datetime, end_date: datetime):
    """
        Creates a report with the data of the tickets printed by a certain user over a pdf file saved on the server in the reports folder from static.
        Returns the path of the created report.
    """
    # Create the path of the report
    report_path = f'static/reports/{user.name}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.pdf'

    # Create the pdf file
    pdf = SimpleDocTemplate(report_path, pagesize=letter)

    # Create the styles for the pdf
    styles = getSampleStyleSheet()
    style = styles['Normal']

    # Create the content of the pdf
    content = []

    # Create the title of the pdf
    title = f'Reporte de boletines del usuario {user.name} desde {start_date.strftime("%Y-%m-%d")} hasta {end_date.strftime("%Y-%m-%d")}'
    content.append(Paragraph(title, style))
    content.append(Spacer(1, 12))

    # Create the table of the pdf
    table_data = [
        ['Zona', 'Cantidad de boletines'],
        ['Pagados con tarjeta', data['paid_by_card']],
        ['Pagados en efectivo', data['paid_by_cash']],
        ['Duración de 30 minutos', data['duration_of_30']],
        ['Duración de 60 minutos', data['duration_of_60']],
        ['Duración de 90 minutos', data['duration_of_90']],
        ['Duración de 120 minutos', data['duration_of_120']],
    ]
    table = Table(table_data)
    content.append(table)

    # Create the pdf
    pdf.build(content)

    # Return the path of the created report
    return report_path