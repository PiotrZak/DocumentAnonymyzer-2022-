from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTTextBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

def to_txt(pdf):

    parser = PDFParser(pdf)
    doc = PDFDocument(parser)
    page = list(PDFPage.create_pages(doc))[0]
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    interpreter.process_page(page)
    layout = device.get_result()

    text = ''
    stack = ''

    for obj in layout:
        if isinstance(obj, LTTextBox):
            text += obj.get_text()

        elif isinstance(obj, LTFigure):
            stack += list(obj)

    return text;
