import os, json, sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_cat(input_files, output_stream):
    input_streams = []
    try:
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        writer = PdfFileWriter() 
        for reader in map(PdfFileReader, input_streams): 
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()


if __name__ == '__main__':

    pdffile1 = '/tmp/'+ sys.argv[1]
    pdffile2 = '/tmp/'+ sys.argv[2]
    outputName = '/tmp/' + sys.argv[3]

    inputFileList = []
    inputFileList.append(pdffile1)
    inputFileList.append(pdffile2)
    print inputFileList

    output_stream = open(outputName, 'wb')
    pdf_cat(inputFileList, output_stream)
