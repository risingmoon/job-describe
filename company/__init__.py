import requests

from bs4 import BeautifulSoup
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, ListFlowable
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


class JobDescription:
    """Base class for job description"""

    def __init__(self, url):
        request = requests.get(url)
        self.soup = BeautifulSoup(request.text, 'html.parser')

    @property
    def title(self):
        raise NotImplemented()

    @property
    def location(self):
        raise NotImplemented()

    @property
    def summary(self):
        raise NotImplemented()

    @property
    def responsibilities(self):
        raise NotImplemented()

    @property
    def qualifications(self):
        raise NotImplemented()

    @property
    def benefits(self):
        raise NotImplemented()


styles = getSampleStyleSheet()
STYLE_H1 = styles['Heading1']
STYLE_H2 = styles['Heading2']
STYLE_N = styles['Normal']


class Document:

    def __init__(self):
        self.story = []
        filename = self.get_filename()
        self.doc = SimpleDocTemplate('%s.pdf' % filename)

    def get_filename(self):
        raise NotImplemented()

    def add_heading(self, content, heading):
        self.story.append(Paragraph(content, heading))

    def add_body(self, body):
        for p in body.split('\n'):
            if p:
                self.story.append(Paragraph(p, STYLE_N))
            else:
                self.add_space()

    def add_space(self):
        self.story.append(Spacer(1, 0.2 * inch))

    def add_table(self, data):
        self.add_space()
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black)
        ])
        table = Table(data)
        table.setStyle(table_style)
        self.story.append(table)
        self.add_space()

    def add_unordered_list(self, unordered_list):
        items = []
        for item in unordered_list:
            items.append(Paragraph(item, STYLE_N))
        self.story.append(ListFlowable(items, bulletType='bullet'))

    def debug(self):
        raise NotImplemented()
