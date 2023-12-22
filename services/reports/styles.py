from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle

class Styles:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def title(self):
        title_style = self.styles['Heading1']
        title_style.alignment = 0
        return title_style

    def subtitle(self):
        subtitle_style = self.styles['Heading2']
        subtitle_style.alignment = 0
        return subtitle_style

    def table(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('PADDING', (0, 0), (-1, 0), 20),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.toColor('#f8fff7')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.toColor('#00240a')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ])
    
    def table2(self):
        return TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('PADDING', (0, 0), (-1, 0), 20),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BACKGROUND', (0, 0), (-1, -1), colors.toColor('#45a584')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.toColor('#00240a')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ])

    def table3(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('PADDING', (0, 0), (-1, 0), 20),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.toColor('#FFFFFF')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.toColor('#00240a')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
