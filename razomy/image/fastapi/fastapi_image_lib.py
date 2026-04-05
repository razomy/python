from typing import Annotated
from fastapi import File
from fastapi.responses import Response
from io import BytesIO

from razomy.python.image import image_lib


def fastapi_image_post(image: Annotated[bytes, File(description="A file read as bytes")]):
    image_data = BytesIO(image)
    image_buffer = image_lib.to_jpeg(image_data)
    return Response(content=image_buffer.getvalue(), media_type='image/jpeg')
