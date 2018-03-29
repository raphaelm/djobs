import copy

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils.functional import cached_property
from io import BytesIO

from django.utils.html import escape
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import pagesizes, utils
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, KeepInFrame, FrameBreak, Spacer, Image
from urllib.parse import urljoin

from djobs.core.models import JobOpening


class PDFGenerator:
    pagesize = pagesizes.landscape(pagesizes.A5)

    def __init__(self, obj: JobOpening):
        self.obj = obj

    @staticmethod
    def _init_fonts():
        pdfmetrics.registerFont(TTFont('Gandhi-R', finders.find('font/GandhiSans-Regular-webfont.ttf')))
        pdfmetrics.registerFont(TTFont('Gandhi-BI', finders.find('font/GandhiSans-BoldItalic-webfont.ttf')))
        pdfmetrics.registerFont(TTFont('Gandhi-I', finders.find('font/GandhiSans-Italic-webfont.ttf')))
        pdfmetrics.registerFont(TTFont('Gandhi-B', finders.find('font/GandhiSans-Bold-webfont.ttf')))
        pdfmetrics.registerFontFamily('Gandhi', normal='Gandhi-R', bold='Gandhi-B',
                                      italic='Gandhi-I', boldItalic='Gandhi-BI')

    @cached_property
    def stylesheet(self):
        stylesheet = StyleSheet1()
        stylesheet.add(ParagraphStyle(name='Normal', fontName='Gandhi-R', fontSize=10, leading=12))
        stylesheet.add(ParagraphStyle(name='Heading1', fontName='Gandhi-B', fontSize=16, leading=20))
        stylesheet.add(ParagraphStyle(name='Meta', fontName='Gandhi-I', fontSize=10, leading=12))
        stylesheet.add(ParagraphStyle(name='Message', spaceBefore=2 * mm, parent=stylesheet['Normal']))
        return stylesheet

    def build_doc(self, fhandle):
        def text(s):
            return escape(s).replace("\n", "<br/>")

        doc = BaseDocTemplate(fhandle, pagesize=self.pagesize)
        frames = [
            Frame(
                15 * mm,
                15 * mm,
                100 * mm,
                120 * mm,
                leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                id='normal',
            ),
            Frame(
                125 * mm,
                25 * mm,
                70 * mm,
                110 * mm,
                leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                id='normal'
            ),
        ]
        doc.addPageTemplates([
            PageTemplate(id='AllPages', frames=frames, pagesize=self.pagesize,
                         onPage=self._draw_qr)
        ])

        meta = []
        if self.obj.job_location:
            meta.append('Location: {}'.format(self.obj.job_location))
        if self.obj.job_remote:
            meta.append('Remote')
        if self.obj.job_salary_range:
            meta.append('Salary: {}'.format(self.obj.job_salary_range))
        meta = ' · '.join(meta)

        company_story = []
        if self.obj.logo:
            im = Image(
                os.path.join(settings.MEDIA_ROOT, self.obj.logo.name),
                height=35 * mm
            )
            im._restrictSize(70 * mm, 35 * mm)
            company_story.append(im)
            company_story.append(Spacer(1 * mm, 3 * mm))

        company_story.append(
            Paragraph(text(self.obj.company_name), style=self.stylesheet['Heading1']),
        )
        company_story.append(
            Paragraph(text(self.obj.company_description), style=self.stylesheet['Normal']),
        )
        if self.obj.company_contact:
            company_story.append(Spacer(1 * mm, 3 * mm))
            company_story.append(
                Paragraph('Contact', style=self.stylesheet['Heading1']),
            )
            company_story.append(
                Paragraph(text(self.obj.company_contact), style=self.stylesheet['Normal']),
            )

        doc.build([
            KeepInFrame(110 * mm, 120 * mm, [
                Paragraph(text(self.obj.job_title), style=self.stylesheet['Heading1']),
                Spacer(1 * mm, 2 * mm),
                Paragraph(text(meta), style=self.stylesheet['Meta']),
                Spacer(1 * mm, 2 * mm),
                Paragraph(text(self.obj.job_description), style=self.stylesheet['Normal'])
            ], mode='truncate'),
            FrameBreak(),
            KeepInFrame(70 * mm, 110 * mm, company_story, mode='truncate')
        ])

    def _draw_qr(self, canvas, doc):
        canvas.saveState()

        qrw = QrCodeWidget(
            urljoin(settings.SITE_URL, reverse('job.detail', kwargs={'pk': self.obj.pk})),
            barHeight=20 * mm, barWidth=20 * mm
        )
        d = Drawing(20 * mm, 20 * mm)
        d.add(qrw)
        qr_x = 175 * mm
        qr_y = 2.2 * mm
        renderPDF.draw(d, canvas, qr_x, qr_y)

        canvas.restoreState()

    def create_pdf(self, background=True):
        buffer = BytesIO()
        self.build_doc(buffer)
        buffer.seek(0)

        new_pdf = PdfFileReader(buffer)
        output = PdfFileWriter()
        bgf = open(finders.find('background.pdf'), "rb")
        bg_pdf = PdfFileReader(bgf)

        for page in new_pdf.pages:
            bg_page = copy.copy(bg_pdf.getPage(0))
            bg_page.mergePage(page)
            output.addPage(bg_page)

        output.addMetadata({
            '/Title': 'Preview',
            '/Creator': 'djobs',
        })
        outbuffer = BytesIO()
        output.write(outbuffer)
        outbuffer.seek(0)
        return outbuffer.read()


PDFGenerator._init_fonts()
