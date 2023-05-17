
from PyPDF2 import PdfReader, PdfWriter


file_name = "Theory, design, and applications of unmanned aerial vehicles ( PDFDrive ).pdf"

def main(file_name):
    reader = PdfReader(file_name)
    writer, writer2 = PdfWriter(), PdfWriter()
    for page in reader.pages[213:246]:
        writer.add_page(page)
    for page in reader.pages[245:274]:
        writer2.add_page(page)

    writer.add_metadata(reader.metadata)
    writer2.add_metadata(reader.metadata)
    with open("condensed.pdf", "wb") as fp:
        page.compress_content_streams()
        writer.write(fp)
    with open("condensed2.pdf", "wb") as fp:
        page.compress_content_streams()
        writer2.write(fp)
        # print(page.extract_text())


if __name__  == "__main__":
    main(file_name)