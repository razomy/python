from PIL import Image
from rembg import remove
from io import BytesIO
from pathlib import Path


def compress_image(file_path, quality=10):
    try:
        with Image.open(file_path) as img:
            img.save(file_path, optimize=True, quality=quality)
        print(f"Compressed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_folder(directory):
    image_extensions = {".jpg", ".jpeg", ".png", ".webp"}  # Supported formats

    for file_path in Path(directory).rglob("*"):
        if file_path.suffix.lower() in image_extensions:
            compress_image(file_path)

def to_jpeg(image_data: BytesIO):
    image = Image.open(image_data)
    image_buffer = BytesIO()
    image.convert('RGB').save(image_buffer, format='JPEG', quality=100)
    return image_buffer


def remove_background(input_path):
    return remove(input_path)
