import os, sys, json, re
from tika import parser
import PyPDF2
from PyPDF2 import PdfFileReader
import nltk

def pdf2text():
    try:
        raw = parser.from_file('sample2.pdf')
        #raw = str(raw)
        #safe_text = raw.encode('utf-8', errors='ignore')
        #safe_text1 = str(safe_text).replace("\n", "").replace("\\", "")
        #print safe_text1
        content = raw['content']
        print content

        a = content
        words = nltk.tokenize.word_tokenize(a)
        fd = nltk.FreqDist(words)
        fd.plot()



        pdfFileObject = open('sample.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        count = pdfReader.numPages
        for i in range(count):
            page = pdfReader.getPage(i)
            #print(page.extractText())
    except Exception as er:
        print "pdf2text convertion exception :: %s"%er

def pyPDF2text():
    try:
        with open('sample.pdf', 'rb') as f:
            pdf = PdfFileReader(f)

            page = pdf.getPage(0)

            text = page.extractText()
            print(text)


    except Exception as eR:
        print "pyPDF2Text Exception as :: %s"%eR

if __name__ == "__main__":

    pdf2text()




    
