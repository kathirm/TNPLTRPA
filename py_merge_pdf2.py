import os, sys
from PyPDF2 import PdfFileMerger

def merge_pdf():
    try:
        pdfs = ['Ashwin Kumar_profile.pdf', 'Y.pdf']
        merger = PdfFileMerger()
        for pdf in pdfs:
             merger.append(open(pdf, 'rb'))
        with open ('result.pdf', 'wb') as fout:
            merger.write(fout)
    except Exception as er:
        print er

if __name__ == "__main__":
 
    merge_pdf()
