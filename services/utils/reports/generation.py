from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
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
    
    #Increase the width of the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 18),
        ('FONTSIZE', (0, 0), (1, -1), 14),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        
    ])
    



    # Create the title of the pdf
    title = f'Reporte del usuario {user.name} desde {start_date.strftime("%Y-%m-%d")} hasta {end_date.strftime("%Y-%m-%d")}'
    
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 12))

    subtitle_style.alignment = 1
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

    left_margin = 0.4 * inch  # for example, 0.5 inches left margin
    right_margin = 0.4 * inch 
    top_margin = 0.4 * inch
    bottom_margin = 0.4 * inch

    # Create the pdf file with adjusted margins
    pdf = SimpleDocTemplate(report_path, pagesize=letter, title=pdf_title, 
                            leftMargin=left_margin, rightMargin=right_margin, 
                            topMargin=top_margin, bottomMargin=bottom_margin)


    # Create the styles for the pdf
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 16

    # Create the content of the pdf
    content = []

    # Defining styles
    title_style = styles['Heading1']
    title_style.fontSize = 14
    subtitle_style = styles['Heading2']
    subtitle_style.fontSize = 12
    subtitle_style.fontName = 'Helvetica'
    text_style = styles['Normal']
    text_style.fontSize = 10

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])

    # Create the title of the pdf
    title = f'Reporte de la zona {zone.name} desde {start_date.strftime("%Y-%m-%d")} hasta {end_date.strftime("%Y-%m-%d")}'
    
    content.append(Paragraph(title, title_style))
    content.append(Spacer(1, 8))

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

    tickets_table = Table(tickets_data, colWidths=[260, 180], rowHeights=25)
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
    
    bulletins_table = Table(bulletins_data, colWidths=[260, 180], rowHeights=25)
    bulletins_table.setStyle(table_style)
    content.append(bulletins_table)
    
    # Create the pdf
    pdf.build(content)

    # Return the path of the created report
    return report_path



class generationManager:
    def __init__(self, start_date, end_date, zone=None, user=None):
        self.start_date = start_date
        self.end_date = end_date
        self.zone = zone
        self.user = user

        self.content = []
        self.styles = getSampleStyleSheet()
    
    def get_tickets_data(self):
        if self.zone:
            tickets = TicketModel.get_tickets_by_zone(self.zone.id, self.start_date, self.end_date)
        elif self.user:
            tickets = TicketModel.get_tickets_by_user(self.user.id, self.start_date, self.end_date)
        else:
            tickets = TicketModel.get_tickets_by_date(self.start_date, self.end_date)
        
        tickets_attributes_count = get_tickets_attributes_count(tickets)
        
        return tickets_attributes_count
    
    def generate_tickets_report(self):
        tickets_data = self.get_tickets_data()
        self.content.append(self.get_title(f'Reporte de tickets desde {self.start_date.strftime("%Y-%m-%d")} hasta {self.end_date.strftime("%Y-%m-%d")}'))
        self.content.append(Spacer(1, 8))
        self.content.append(self.get_subtitle(f'Tickets registrasos'))
        self.content.append(self.get_table(self.get_tickets_table_data(tickets_data), col_widths=[260, 180], row_heights=25, table_style=self.get_table_style()))
        return self.content
    
    def get_bulletins_table_data(self, bulletins_data):
        return [
        ['Modo', 'Cantidad de boletines'],
        ['Pagados', bulletins_data['paid']],
        ['Aún por pagar', bulletins_data['not_paid']],
        ['Duración de 30 minutos', bulletins_data['duration_of_30']],
        ['Ingresos por boletines de 30 minutos', f"{bulletins_data['total_income_by_30']} €"],
        ['Duración de 60 minutos', bulletins_data['duration_of_60']],
        ['Ingresos por boletines de 60 minutos', f"{bulletins_data['total_income_by_60']} €"],
        ['Duración de 90 minutos', bulletins_data['duration_of_90']],
        ['Ingresos por boletines de 90 minutos', f"{bulletins_data['total_income_by_90']} €"],
        ['Duración de 120 minutos', bulletins_data['duration_of_120']],
        ['Ingresos por boletines de 120 minutos', f"{bulletins_data['total_income_by_120']} €"],
        ['Total de ingresos',f"{bulletins_data['total_income']} €"],
    ]
    
    def get_tickets_table_data(self, tickets_data):
        return [
        ['Modo', 'Cantidad de tickets'],
        ['Pagados con tarjeta', tickets_data['paid_by_card']],
        ['Pagados en efectivo', tickets_data['paid_by_cash']],
        ['Duración de 30 minutos', tickets_data['duration_of_30']],
        ['Ingresos por tickets de 30 minutos', f"{tickets_data['total_income_by_30']} €"],
        ['Duración de 60 minutos', tickets_data['duration_of_60']],
        ['Ingresos por tickets de 60 minutos', f"{tickets_data['total_income_by_60']} €"],
        ['Duración de 90 minutos', tickets_data['duration_of_90']],
        ['Ingresos por tickets de 90 minutos', f"{tickets_data['total_income_by_90']} €"],
        ['Duración de 120 minutos', tickets_data['duration_of_120']],
        ['Ingresos por tickets de 120 minutos', f"{tickets_data['total_income_by_120']} €"],
        ['Total de ingresos', f"{tickets_data['total_income']} €"],
    ]
    

    def get_title(self, title_text, size: int = 0):
        title_style = self.styles['Heading1']
        title_style.fontSize = 14 + (size*2)
        title.style.color = colors.black
        title = Paragraph(title_text, title_style)
        return title
    
    def get_subtitle(self, subtitle_text, size: int = 0):
        subtitle_style = self.styles['Heading2']
        subtitle_style.fontSize = 12 + (size*2)
        subtitle_style.fontWeight = 1
        subtitle = Paragraph(subtitle_text, subtitle_style)
        return subtitle
    
    def get_text(self, text, size: int = 0):
        text_style = self.styles['Normal']
        text_style.fontSize = 10 + (size*2)
        text = Paragraph(text, text_style)
        return text
    
    def get_table(self, data, col_widths, row_heights, table_style):
        table = Table(data, colWidths=col_widths, rowHeights=row_heights)
        table.setStyle(table_style)
        return table