from django.shortcuts import render
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .exceptions import FileUploadError
from .serializers import CustomImageSerializer
from .service import upload_image, get_image_count


class ImageHandler(APIView):
    """
    Вьюшка для обработки get/post запроса изображений.

    get - рендер страницы.
    post - запрос на добавление изображения в бд.

    Бросает FileUploadError в случае невалидного расширения файла или IO ошибки.

    """
    permission_classes = ()
    authentication_classes = ()
    extensions = ['jpg', 'png']

    def check_file_extension(self, file_obj):
        ext = file_obj.name.split('.')[-1]
        if ext not in self.extensions:
            raise FileUploadError('File extension "{}" not in possible file extensions {}'.format(
                ext, self.extensions)
            )

    def get(self, request):
        image_count = get_image_count()
        return render(request, 'index.html', context={'count': image_count, 'extensions': self.extensions})

    def post(self, request):
        file = request.FILES['file']
        try:
            self.check_file_extension(file)
            img = upload_image(file)
            return Response({'status': 'ok', 'file': CustomImageSerializer(img).data}, status=HTTP_200_OK)
        except FileUploadError as e:
            return Response({'status': 'error', 'msg': str(e)}, status=HTTP_400_BAD_REQUEST)
