from io import BytesIO
from PIL import Image


def create_dummy_txt(filename: str = "dummy.txt") -> BytesIO:
    txt_file = BytesIO()
    txt_file.write(b"0" * 10)
    txt_file.name = filename
    txt_file.seek(0)
    return txt_file


def create_dummy_img(filename: str = "dummy", file_type: str = "png") -> BytesIO:
    image_data = BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(image_data, format=file_type)
    image_data.name = f"{filename}.{file_type}"
    image_data.seek(0)
    return image_data


def create_dummy_video(filename: str = "dummy.mp4") -> BytesIO:
    return create_dummy_txt(filename)
