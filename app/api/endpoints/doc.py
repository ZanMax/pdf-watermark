import base64
import os
from datetime import datetime
from typing import Any

import aiofiles
from fastapi import APIRouter, Form, HTTPException
from fastapi import File, UploadFile

from app.watermark import Watermark

router = APIRouter()

APP_ROOT = os.path.dirname(os.path.abspath('main.py'))
WORK_DIR = os.path.join(APP_ROOT, 'app/tmp/upload')


@router.post("/doc/create", response_model=Any)
async def create_new_doc(headertext: str = Form(''), converturl: str = Form(...), convert_type: str = Form(...),
                         docx: UploadFile = File(...), watermark: UploadFile = File(...), logo: UploadFile = File(...),
                         convert: UploadFile = File(...)) -> Any:
    now = datetime.now()
    time_stamp = str(int(datetime.timestamp(now)))

    if converturl:
        docx_file = os.path.join(WORK_DIR, f'{time_stamp}_{docx.filename}')
        async with aiofiles.open(docx_file, 'wb') as f:
            content = await docx.read()
            await f.write(content)

        watermark_file = os.path.join(WORK_DIR, f'{time_stamp}_{watermark.filename}')
        async with aiofiles.open(watermark_file, 'wb') as f:
            content = await watermark.read()
            await f.write(content)

        logo_file = os.path.join(WORK_DIR, f'{time_stamp}_{logo.filename}')
        async with aiofiles.open(logo_file, 'wb') as f:
            content = await logo.read()
            await f.write(content)

        convert_file = os.path.join(WORK_DIR, f'{time_stamp}_{convert.filename}')
        async with aiofiles.open(convert_file, 'wb') as f:
            content = await convert.read()
            await f.write(content)

        result_pdf = Watermark().create_watermark_pdf(docx_file, watermark_file, convert_file, converturl, logo_file,
                                                      headertext, convert_type)
        # result_pdf = 'app/tmp/final.pdf'
        with open(result_pdf, 'rb') as f:
            blob = base64.b64encode(f.read())

        return {'file_blob': blob, 'media_type': 'application/pdf', 'filename': 'final.pdf'}
    else:
        raise HTTPException(status_code=404, detail="Some item not found")
