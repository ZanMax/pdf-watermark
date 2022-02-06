import os.path
from datetime import datetime

from app.utils import convert_docx_to_pdf, add_watermark_to_pdf, watermark_image_to_pdf, pdf_to_jpg, \
    image_to_pdf, create_convert_elements_pdf, merge_pdf_read_only_and_convert

APP_ROOT = os.path.dirname(os.path.abspath('main.py'))


class Watermark:
    def __init__(self):
        self.docx_file_name = ''
        self.pdf_file_name = ''
        self.wtm_pdf = ''
        self.read_only_wtm_pdf = ''
        self.watermark_file = ''
        self.convert_type = ''
        self.cur_timestamp = str(int(datetime.timestamp(datetime.now())))
        self.tmp_dir = os.path.join(APP_ROOT, 'app/tmp')

        self.work_path = os.path.join(self.tmp_dir, self.cur_timestamp)
        self.pdf_images_path = os.path.join(self.work_path, 'images')

        try:
            os.mkdir(self.work_path)
        except OSError:
            print("Creation of the directory %s failed" % self.work_path)

    def create_watermark_pdf(self, file_name, watermark_image, image, link, logo, text, convert_type):
        if watermark_image and os.path.isfile(watermark_image):
            watermark_image_to_pdf(watermark_image, self.work_path)
            self.watermark_file = os.path.join(self.work_path, 'watermark.pdf')
        else:
            raise Exception('Empty watermark file or file not exist')

        if file_name and os.path.isfile(file_name):
            self.docx_file_name = file_name
            self.doc2pdf()
        else:
            raise Exception('Empty docx file or file not exist')

        self.watermark_pdf()
        self.pdf_read_only()
        self.add_convert_elements(self.work_path, image, link, logo, text, convert_type)
        self.crate_final_pdf(self.work_path, self.read_only_wtm_pdf)

        final_pdf = os.path.join(self.work_path, 'final.pdf')
        if os.path.isfile(final_pdf):
            return final_pdf
        raise {'error': 'PDF generation error'}

    def doc2pdf(self):
        self.pdf_file_name = convert_docx_to_pdf(self.docx_file_name, self.work_path)

    def watermark_pdf(self):
        if self.pdf_file_name and os.path.isfile(self.pdf_file_name):
            filename, file_extension = os.path.splitext(os.path.basename(self.pdf_file_name))
            result_wtm_pdf = f'{filename}_wtm.{file_extension}'
            self.wtm_pdf = os.path.join(self.work_path, result_wtm_pdf)
            add_watermark_to_pdf(self.pdf_file_name, self.wtm_pdf, self.watermark_file)

    def pdf_read_only(self):
        try:
            os.mkdir(self.pdf_images_path)
        except OSError:
            print("Creation of the directory %s failed" % self.work_path)

        filename, file_extension = os.path.splitext(os.path.basename(self.wtm_pdf))
        result_ro_pdf = f'{filename}_ro.{file_extension}'
        self.read_only_wtm_pdf = os.path.join(self.work_path, result_ro_pdf)

        pdf_to_jpg(self.wtm_pdf, self.pdf_images_path)
        image_to_pdf(self.pdf_images_path, self.read_only_wtm_pdf)

    def add_convert_elements(self, path, image, link, logo, text, convert_type):
        if os.path.isfile(image) and os.path.isfile(logo):
            create_convert_elements_pdf(path, image, link, logo, text, convert_type)
        else:
            raise Exception('Convert image or logo not exist')

    def crate_final_pdf(self, path, ro_pdf):
        merge_pdf_read_only_and_convert(path, ro_pdf)
