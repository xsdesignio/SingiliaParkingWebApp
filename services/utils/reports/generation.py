from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle


def _get_report_path_and_title(subject, start_date, end_date, folder='reports'):
    formatted_start = start_date.strftime("%Y-%m-%d")
    formatted_end = end_date.strftime("%Y-%m-%d")
    file_name = f"{subject.name.replace(' ', '-')}-{formatted_start}-{formatted_end}.pdf"
    path = f'static/{folder}/{file_name}'
    title = f'reporte-{translation(subject.__class__.__name__)}-{file_name}'
    return path, title

def _initialize_pdf(report_path, pdf_title):
    left_margin = 0.4 * inch
    right_margin = 0.4 * inch
    top_margin = 0.4 * inch
    bottom_margin = 0.4 * inch

    pdf = SimpleDocTemplate(report_path, pagesize=letter, title=pdf_title, 
                            leftMargin=left_margin, rightMargin=right_margin, 
                            topMargin=top_margin, bottomMargin=bottom_margin)
    return pdf

def _create_content(subject_name, subject_type, data_categories, data, start_date, end_date):
    styles = getSampleStyleSheet()

    # Styles
    title_style = styles['Heading1']
    title_style.alignment = 1
    subtitle_style = styles['Heading2']
    subtitle_style.alignment = 1
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('PADDING', (0, 0), (-1, 0), 20),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.toColor('#edfff2')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.toColor('#00240a')),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    content = []
    title = f'Reporte {subject_type} {subject_name}'
    subtitle = f'Periodo {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}'

    content.append(Paragraph(title, title_style))
    content.append(Paragraph(subtitle, subtitle_style))

    content.append(Spacer(1, 8))

    print(data_categories)

    for category in data_categories:
        print(category)
        subtitle = f'Cuadrante {translation(category)} de aparcamiento {subject_name}'
        content.append(Paragraph(subtitle, subtitle_style))

        content.append(Spacer(1, 18))

        table_data = [['Modo', f'Cantidad de {translation(category)}']]


        category_data = data[category]
        # Checking for payment status if the category is bulletins
        if(category == "bulletins"):
            table_data += [
                ['Cantidad total', category_data['bulletins_amount']],
                ['Pagados', category_data['paid_amount']],
                ['Aún por pagar', category_data['not_paid_amount']],
                ['Pagados con tarjeta', category_data['paid_by_card']],
                ['Pagados en efectivo', category_data['paid_by_cash']]
            ]

        if(category == "tickets"):
            table_data += [
                ['Cantidad total', category_data['tickets_amount']],
                ['Pagados con tarjeta', category_data['paid_by_card']],
                ['Pagados en efectivo', category_data['paid_by_cash']]
            ]

        
        table = Table(table_data, colWidths=[260, 200], rowHeights=30)

        table.setStyle(table_style)
        content.append(table)


        content.append(Spacer(1, 28))


        subtitle = f'Resultados según duración'
        content.append(Paragraph(subtitle, subtitle_style))

        content.append(Spacer(1, 18))

        
        for duration_data in category_data["data_by_duration"]:
            content.append(Spacer(1, 18))
            subtitle = f'Resultados de { duration_data["duration"] }'

            content.append(Paragraph(subtitle, subtitle_style))

            table_data = [
                    [f'Cantidad de {translation(category)}: ', duration_data["amount"]],
                    [f'Pagados con tarjeta: ', duration_data["paid_by_card"]],
                    [f'Pagados en efectivo: ', duration_data["paid_by_cash"]],
                    [f'Ingresos por {translation(category)}: ', f"{duration_data['total_income']} €"],
                ]
            
            duration_table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('PADDING', (0, 0), (-1, 0), 20),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.toColor('#E1FFFF')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.toColor('#00240a')),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
        
            table = Table(table_data, colWidths=[260, 200], rowHeights=30)

            table.setStyle(duration_table_style)
            content.append(table)

        content.append(Spacer(1, 40))

    return content

def create_report(subject, start_date, end_date, data, subject_type):
    report_path, pdf_title = _get_report_path_and_title(subject, start_date, end_date)
    
    pdf = _initialize_pdf(report_path, pdf_title)
    data_categories = list(data.keys())
    content = _create_content(subject.name, subject_type, data_categories, data, start_date, end_date)
    pdf.build(content)
    return report_path

def create_report_for_user(data, user, start_date, end_date):
    return create_report(user, start_date, end_date, data, "usuario")

def create_report_for_zone(data, zone, start_date, end_date):
    return create_report(zone, start_date, end_date, data, "zona")



def translation(string):

    if string == "Zone":
        return "Zona"
    if string == "User":
        return "Usuario"
    
    if string == "tickets":
        return "Tickets"

    if string == "bulletins":
        return "Boletines"
    
    