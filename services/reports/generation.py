from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table
from .styles import Styles
from services.users.entities import User
from services.zones.entities import Zone

from .utils import translate


def _get_report_path_and_title(subject, start_date, end_date, folder='reports'):
    formatted_start = start_date.strftime("%Y-%m-%d")
    formatted_end = end_date.strftime("%Y-%m-%d")
    file_name = f"{subject.name.replace(' ', '-')}-{formatted_start}-{formatted_end}.pdf"
    path = f'static/{folder}/{file_name}'
    title = f'reporte-{translate(subject.__class__.__name__)}-{file_name}'
    return path, title


def _initialize_pdf(report_path, pdf_title):
    scalar = 0.6
    left_margin = scalar * inch
    right_margin = scalar * inch
    top_margin = scalar * inch
    bottom_margin = scalar * inch

    pdf = SimpleDocTemplate(report_path, pagesize=letter, title=pdf_title, 
                            leftMargin=left_margin, rightMargin=right_margin, 
                            topMargin=top_margin, bottomMargin=bottom_margin)
    return pdf


def _create_content(data, user: User, zone: Zone, start_date, end_date) -> list:
    """Create the content to be added to the pdf
    
    Keyword arguments:
    user -- user who owns the data
    zone -- optional. If set, filters the user data by zone
    start
    Return: return_description
    """
    styles = Styles()
    title = f'CONTROLADOR: {user.id} {user.name}'
    content = []
    content.append(Paragraph(title, styles.title()))
    content.append(Spacer(1, 10))

    table_data = get_table(data)
    total_income = data["tickets"]["total_income"] + data["bulletins"]["total_income"]
    table_data.append([
        f'{start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}', zone.name if zone else '', '', f"{total_income} €"
    ])

    table = Table(
        table_data, 
        colWidths=[160, 120], 
        rowHeights=24
    )
    table.setStyle(styles.table())

    table2 = Table(
        [["SUMA TOTAL A INGRESAR", f"{total_income} €"]], 
        colWidths=[400, 120], 
        rowHeights=32
    )
    table2.setStyle(styles.table2())


    subtitle = f"""
    El controlador: {user.name} nº {user.id} ha ingresado el importe 
    de { total_income } € en concepto de recaudación zona S.M.E.R, en la
    c/c 2103 3042 20 0030001171, de unicaja, adjuntándose justificante 
    de abono en cuenta"""

    table3 = Table(
        [["Firma del controlador", "Observaciones"],
         ["", ""]], 
        colWidths=[140, 380], 
        rowHeights=[24, 100]
    )
    table3.setStyle(styles.table3())

    content.append(table)
    content.append(Spacer(1, 10))
    content.append(table2)
    content.append(Spacer(1, 10))
    content.append(Paragraph(subtitle, styles.subtitle()))

    content.append(Spacer(1, 10))
    content.append(table3)

    return content


def get_table(data) -> list[list[str]]:
    table_data = [['Duración', 'Precio con IVA', 'Cantidad', 'Importe total']]
        
    for category in list(data.keys()):
        table_data.append([translate(category), "", "", ""])

        for duration_data in data[category]["data_by_duration"]: 
            table_data.append([
                duration_data["duration"], 
                f'{duration_data["price"]} €', 
                duration_data["amount"], 
                f"{duration_data['total_income']} €"
            ])
        

    return table_data
    


def create_report(data, user, zone, start_date, end_date):
    report_path, pdf_title = _get_report_path_and_title(user, start_date, end_date)
    
    pdf = _initialize_pdf(report_path, pdf_title)
    content = _create_content(data, user, zone, start_date, end_date)
    pdf.build(content)

    return report_path




    
    