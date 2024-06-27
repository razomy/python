from PIL import Image
from rembg import remove
from io import BytesIO


def to_jpeg(image_data: BytesIO):
    image = Image.open(image_data)
    image_buffer = BytesIO()
    image.convert('RGB').save(image_buffer, format='JPEG', quality=100)
    return image_buffer


def remove_background(input_path):
    return remove(input_path)
