from django.shortcuts import redirect


def index(request):
    """
    Заглушка на стартовую страницу, хотя лучше на уровне middleware сделать
    :param request:
    :return:
    """
    return redirect('/image')
