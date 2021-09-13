from .exceptions import FileUploadError
from .models import CustomImage
from PIL import Image
from uuid import uuid4
from DRFImageUploader.settings import MEDIA_ROOT, IMAGE_DEFAULT_SHAPE, IMAGE_DEFAULT_UPLOAD_SIZE
import os


def get_image_count() -> int:
    """
    Возвращает количество записей в бд
    :return: int
    """
    return CustomImage.objects.count()


def write_file(file_obj) -> str:
    """
    Осуществляет запись файла.

    :param file_obj: UploadedFile - файл, принимаемый из реквеста
    :return: str - Путь к файлу
    """
    file_dist = os.path.join(MEDIA_ROOT, str(uuid4())) + '.' + file_obj.name.split('.')[-1]
    with open(file_dist, 'wb+') as f:
        for chunk in file_obj:
            f.write(chunk)
    return file_dist


def process_image(img_path: str) -> None:
    """
    Осуществляет ресайз изображения к дефолтным размерам.

    :param img_path: str - путь к файлу изображения
    :return: None
    """
    img = Image.open(img_path)
    img = img.resize(IMAGE_DEFAULT_SHAPE)
    img.save(img_path)


def upload_image(file_obj) -> CustomImage:
    """
    Осуществляет запись и обработку изображения. В случае ошибки выбрасывает FileUploadError.

    :param file_obj: UploadedFile - файл, принимаемый из реквеста
    :return: CustomImage
    """
    try:
        file_dist = write_file(file_obj)
        process_image(file_dist)
    except IOError:
        raise FileUploadError('I/O error occurred')
    obj = CustomImage.objects.create(file=file_dist, file_name=file_obj.name)
    return obj
