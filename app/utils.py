import os
import os.path
import re
import subprocess
import sys

import img2pdf
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from fpdf import FPDF, HTMLMixin


def convert_image_format(in_image, out_image):
    image = Image.open(in_image)
    image = image.convert('RGB')
    image.save(out_image)


def convert_image_to_pdf(in_image, work_path):
    if os.path.isfile(in_image):
        image = Image.open(in_image)
        image = image.convert('RGB')
        image.save(f"{work_path}/watermark.pdf")
    else:
        raise Exception('Empty watermark image or file not exist')


def watermark_image_to_pdf(image, work_path):
    if os.path.isfile(image):
        a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
        layout_fun = img2pdf.get_layout_fun(a4)
        with open(f"{work_path}/watermark.pdf", "wb") as wtm_pdf, open(image, "rb") as wtm_image:
            img2pdf.convert(wtm_image, outputstream=wtm_pdf, layout_fun=layout_fun)
    else:
        raise Exception('Empty watermark image or file not exist')


def add_watermark_to_pdf(input_pdf, output_pdf, watermark):
    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for i in range(pdf_reader.getNumPages()):
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        page = pdf_reader.getPage(i)
        watermark_page.mergePage(page)
        pdf_writer.addPage(watermark_page)

    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)


def pdf_to_jpg(pdf_file, out_dir='tmp'):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    pages = convert_from_path(pdf_file, 300)
    for i, page in enumerate(pages):
        page.save(f'{out_dir}/{i}.jpg', 'JPEG')


def image_to_pdf(out_dir='out_img', out_pdf='out/output_from_img.pdf'):
    a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4)
    img_list = []
    for i in os.listdir(out_dir):
        path = os.path.join(out_dir, i)
        img_list.append(path)

    with open(out_pdf, "wb") as f:
        f.write(img2pdf.convert(sorted(img_list), layout_fun=layout_fun))


def convert_docx_to_pdf(docx_file, out_folder, timeout=None):
    cmd = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', out_folder, docx_file]
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)


def libreoffice_exec():
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


class PDF(FPDF, HTMLMixin):
    def __init__(self, img, link, logo, text):
        super().__init__()
        self.convert_link = link
        self.convert_img = img
        self.convert_logo = logo
        self.convert_text = text

    def header(self):
        # Logo
        self.image(self.convert_logo, 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, self.convert_text, 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_xy(17, -70)
        self.write_html(f'<a href="{self.convert_link}"><img width="500" height="200" src="{self.convert_img}"></a>')


class PDFConvertCenter(FPDF, HTMLMixin):
    def __init__(self, img, link, logo):
        super().__init__()
        self.convert_link = link
        self.convert_img = img
        self.convert_logo = logo

    def header(self):
        # Logo
        self.image(self.convert_logo, 90, 8, 33)
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_xy(17, -130)
        self.write_html(
            f'<a href="{self.convert_link}"><img width="500" height="200" src="{self.convert_img}"></a>')


def create_convert_elements_pdf(work_dir, img, link, logo, text, convert_type):
    if convert_type == '2':
        pdf = PDFConvertCenter(img, link, logo)
    else:
        pdf = PDF(img, link, logo, text)
    pdf.set_font_size(16)
    pdf.add_page()
    file_path = os.path.join(work_dir, 'convert.pdf')
    pdf.output(file_path)  # <- write to file


def merge_pdf_read_only_and_convert(work_dir, ro_pdf):
    file_path = os.path.join(work_dir, 'convert.pdf')
    convert_pdf = PdfFileReader(file_path)

    # read your existing PDF
    existing_pdf = PdfFileReader(open(ro_pdf, "rb"))

    # add the "watermark" (which is the new pdf) on the existing page
    page_num = existing_pdf.getNumPages()
    output = PdfFileWriter()

    for i in range(page_num):
        if i == 0:
            page = existing_pdf.getPage(0)
            page.mergePage(convert_pdf.getPage(0))
        else:
            page = existing_pdf.getPage(i)
        output.addPage(page)

    # finally, write "output" to a real file
    final_pdf = os.path.join(work_dir, 'final.pdf')
    outputStream = open(final_pdf, "wb")
    output.write(outputStream)
    outputStream.close()
