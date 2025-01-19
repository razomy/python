from PIL import Image

def compress(file_path):
  try:
    with Image.open(file_path) as img:
      img.save(file_path, optimize=True, quality=85)
  except Exception as e:
    print(f"Error processing {file_path}: {e}")
