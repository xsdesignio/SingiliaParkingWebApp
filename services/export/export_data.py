from services.export.file_extensions import FileExtensions
from services.tickets.entities.ticket import Ticket
from services.tickets.models.ticket_model import TicketModel
from services.bulletins.entities.bulletin import Bulletin
from services.bulletins.models.bulletin_model import BulletinModel
import pandas


file_path: str = ""

def export_tickets(tickets: list, extension: FileExtensions) -> str:
    """Create csv or excel file for exported tickets and return the path to the file
    
    Keyword arguments:
    argument: tickets - list of elements returned by database fetch_all over ticket table
    argument: extension - extension and format for the fyle
    Return: return_description
    """


    frame = pandas.DataFrame(tickets)
    path: str

    if extension == FileExtensions.XLSX:
        file_name = "tickets.xlsx"
        path = f'static/exports/{file_name}'
        frame.to_excel(path)
    else:
        file_name = "tickets.csv"
        path = f'static/exports/{file_name}'
        frame.to_csv(path)
    
    return path


def export_bulletins(bulletins: list, extension: FileExtensions) -> str :
    """Create csv or excel file for exported bulletins and return the path to the file
    
    Keyword arguments:
    argument: bulletins - list of elements returned by database fetch_all over bulletin table
    argument: extension - extension and format for the fyle
    Return: return_description
    """

    frame = pandas.DataFrame(bulletins)
    path: str

    if extension == FileExtensions.XLSX:
        file_name = "bulletins.xlsx"
        path = f'static/exports/{file_name}'
        frame.to_excel(path)
    else:
        file_name = "bulletins.csv"
        path = f'static/exports/{file_name}'
        frame.to_csv(path)
    
    return path
