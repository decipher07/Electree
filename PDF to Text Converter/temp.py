import pdfquery
from pdfquery import *
from lxml import etree

pdf = pdfquery.PDFQuery('check.pdf')
pdf.load()

with open('xmltree.xml','wb') as f:
    f.write(etree.tostring(pdf.tree, pretty_print=True))