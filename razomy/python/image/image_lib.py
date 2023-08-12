from PIL import Image
from rembg import remove


def change_format(image, target_type):
    return (Image.open(from_path)
            .convert('RGB')
            .save(target_type))


def remove_background(input_path):
    return remove(input_path)
