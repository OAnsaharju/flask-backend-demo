import io
from PIL import Image
from blurhash import encode


def generate_blurhash(file_data):
    image = Image.open(io.BytesIO(file_data))
    resized_image = image.resize((300, 300))
    rgb_image = resized_image.convert("RGB")
    width, height = rgb_image.size
    pixel_data = list(rgb_image.getdata())
    pixel_data_nested = [pixel_data[i * width : (i + 1) * width] for i in range(height)]
    blurhash_str = encode(pixel_data_nested, 9, 9)

    return blurhash_str
