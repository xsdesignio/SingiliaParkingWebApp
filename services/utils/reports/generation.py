from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle


from datetime import datetime
from services.users.entities.user import User
from services.tickets.models.ticket_model import TicketModel
from services.tickets.controllers.tickets_controller import get_tickets_attributes_count
from services.bulletins.models.bulletin_model import BulletinModel
from services.zones.entities.zone import Zone



# Create function that create a report with the data of the tickets printed by a certain user over a pdf file saved on the server in the reports folder from static.
def create_report_for_user(data: dict, user: User, start_date: datetime, end_date: datetime):
    """
        Creates a report with the data of the tickets printed by a certain user over a pdf file saved on the server in the reports folder from static.
        Returns the path of the created report.
    """
    # Create the path of the report
    report_path = f'static/reports/{user.name}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.pdf'


    pdf_title = f'reporte-usuario-{user.name.replace(" ", "-")}-{start_date.strftime("%Y-%m-%d")}-{end_date.strftime("%Y-%m-%d")}.pdf'

    # Create the pdf file
    pdf = SimpleDocTemplate(report_path, pagesize=letter, title=pdf_title)

    # Create the styles for the pdf
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 18

    # Create the content of the pdf
    content = []


    #Defining styles
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    text_style = styles['Normal']
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 18),
        ('FONTSIZE', (0, 0), (1, -1), 14),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])



    # Create the title of the pdf
    title = f'Reporte del usuario {user.name} desde {start_date.strftime("%Y-%m-%d")} hasta {end_date.strftime("%Y-%m-%d")}'
    
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 12))


    subtitle = f'Tickets registrasos por { user.name }'
    content.append(Paragraph(subtitle, subtitle_style))

    # Create the table of the pdf
    tickets = data["tickets"]
    tickets_data = [
        ['Modo', 'Cantidad de tickets'],
        ['Pagados con tarjeta', tickets['paid_by_card']],
        ['Pagados en efectivo', tickets['paid_by_cash']],
        ['Duración de 30 minutos', tickets['duration_of_30']],
        ['Ingresos por tickets de 30 minutos', f"{tickets['total_income_by_30']} €"],
        ['Duración de 60 minutos', tickets['duration_of_60']],
        ['Ingresos por tickets de 60 minutos', f"{tickets['total_income_by_60']} €"],
        ['Duración de 90 minutos', tickets['duration_of_90']],
        ['Ingresos por tickets de 90 minutos', f"{tickets['total_income_by_90']} €"],
        ['Duración de 120 minutos', tickets['duration_of_120']],
        ['Ingresos por tickets de 120 minutos', f"{tickets['total_income_by_120']} €"],
        ['Total de ingresos', f"{tickets['total_income']} €"],
    ]

    tickets_table = Table(tickets_data, colWidths=[280, 200], rowHeights=30)
    tickets_table.setStyle(table_style)
    content.append(tickets_table)


    subtitle = f'Boletines registrasos por { user.name }'
    content.append(Paragraph(subtitle, subtitle_style))

    # Create the table of the pdf
    bulletins = data["bulletins"]
    bulletins_data = [
        ['Modo', 'Cantidad de boletines'],
        ['Pagados', bulletins['paid']],
        ['Aún por pagar', bulletins['not_paid']],
        ['Duración de 30 minutos', bulletins['duration_of_30']],
        ['Ingresos por boletines de 30 minutos', f"{bulletins['total_income_by_30']} €"],
        ['Duración de 60 minutos', bulletins['duration_of_60']],
        ['Ingresos por boletines de 60 minutos', f"{bulletins['total_income_by_60']} €"],
        ['Duración de 90 minutos', bulletins['duration_of_90']],
        ['Ingresos por boletines de 90 minutos', f"{bulletins['total_income_by_90']} €"],
        ['Duración de 120 minutos', bulletins['duration_of_120']],
        ['Ingresos por boletines de 120 minutos', f"{bulletins['total_income_by_120']} €"],
        ['Total de ingresos',f"{bulletins['total_income']} €"],
    ]
    bulletins_table = Table(bulletins_data, colWidths=[280, 200], rowHeights=30)
    bulletins_table.setStyle(table_style)
    content.append(bulletins_table)
    
    # Create the pdf
    pdf.build(content)

    # Return the path of the created report
    return report_path



    
def create_report_for_zone(data, zone, start_date, end_date):
    """
        Creates a report with the data of the tickets printed in a certain zone over a pdf file saved on the server in the reports folder from static.
        Returns the path of the created report.
    """
    # Create the path of the report
    report_path = f'static/reports/{zone.name}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.pdf'

    pdf_title = f'reporte-zona-{zone.name.replace(" ", "-")}-{start_date.strftime("%Y-%m-%d")}-{end_date.strftime("%Y-%m-%d")}.pdf'
    # Create the pdf file
    pdf = SimpleDocTemplate(report_path, pagesize=letter, title=pdf_title)

    # Create the styles for the pdf
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 18

    # Create the content of the pdf
    content = []


    #Defining styles
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    text_style = styles['Normal']
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 18),
        ('FONTSIZE', (0, 0), (1, -1), 14),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])



    # Create the title of the pdf
    title = f'Reporte de la zona {zone.name} desde {start_date.strftime("%Y-%m-%d")} hasta {end_date.strftime("%Y-%m-%d")}'
    
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 12))


    subtitle = f'Tickets registrasos en la zona { zone.name }'
    content.append(Paragraph(subtitle, subtitle_style))

    # Create the table of the pdf

    tickets = data["tickets"]
    tickets_data = [
        ['Modo', 'Cantidad de tickets'],
        ['Pagados con tarjeta', tickets['paid_by_card']],
        ['Pagados en efectivo', tickets['paid_by_cash']],
        ['Duración de 30 minutos', tickets['duration_of_30']],
        ['Ingresos por tickets de 30 minutos', f"{tickets['total_income_by_30']} €"],
        ['Duración de 60 minutos', tickets['duration_of_60']],
        ['Ingresos por tickets de 60 minutos', f"{tickets['total_income_by_60']} €"],
        ['Duración de 90 minutos', tickets['duration_of_90']],
        ['Ingresos por tickets de 90 minutos', f"{tickets['total_income_by_90']} €"],
        ['Duración de 120 minutos', tickets['duration_of_120']],
        ['Ingresos por tickets de 120 minutos', f"{tickets['total_income_by_120']} €"],
        ['Total de ingresos', f"{tickets['total_income']} €"],
    ]

    tickets_table = Table(tickets_data, colWidths=[280, 200], rowHeights=30)

    tickets_table.setStyle(table_style)
    content.append(tickets_table)


    subtitle = f'Boletines registrasos en { zone.name }'
    content.append(Paragraph(subtitle, subtitle_style))

    # Create the table of the pdf
    bulletins = data["bulletins"]
    bulletins_data = [
        ['Modo', 'Cantidad de boletines'],
        ['Pagados', bulletins['paid']],
        ['Aún por pagar', bulletins['not_paid']],
        ['Duración de 30 minutos', bulletins['duration_of_30']],
        ['Ingresos por boletines de 30 minutos', f"{bulletins['total_income_by_30']} €"],
        ['Duración de 60 minutos', bulletins['duration_of_60']],
        ['Ingresos por boletines de 60 minutos', f"{bulletins['total_income_by_60']} €"],
        ['Duración de 90 minutos', bulletins['duration_of_90']],
        ['Ingresos por boletines de 90 minutos', f"{bulletins['total_income_by_90']} €"],
        ['Duración de 120 minutos', bulletins['duration_of_120']],
        ['Ingresos por boletines de 120 minutos', f"{bulletins['total_income_by_120']} €"],
        ['Total de ingresos',f"{bulletins['total_income']} €"],
    ]
    bulletins_table = Table(bulletins_data, colWidths=[280, 200], rowHeights=30)
    bulletins_table.setStyle(table_style)
    content.append(bulletins_table)
    
    # Create the pdf
    pdf.build(content)

    # Return the path of the created report
    return report_path



    
    