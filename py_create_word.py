import docx


def create_word():
    try:
        doc = docx.Document()
        doc.add_heading('Heading for the document', 0)
        doc.save('demo.docx')

    except Exception as er:
        print "Create new_wordfile Exception error :: %s"%er


if __name__ == "__main__":

    create_word()
