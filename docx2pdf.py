import  os
from win32com import client

#pip instatll win32com
def doc2pdf(doc_name, pdf_name):
    try:
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
        return pdf_name
    except:
        return 1

if __name__=='__main__':
                                                                                                              
    doc_name = "/home/kathir/_py_programs_test/app.docx"
    ftp_name = "/tmp/test.pdf"
    doc2pdf(doc_name, ftp_name)
