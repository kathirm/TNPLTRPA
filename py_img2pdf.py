import sys
import img2pdf
from fpdf import FPDF



pdf = FPDF()
pdfName = "tutorial.pdf"
pdf.output(pdfName)

with open(pdfName,"wb") as f:
    f.write(img2pdf.convert('level2.jpg'))
