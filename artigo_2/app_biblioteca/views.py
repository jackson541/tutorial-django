from django.http import HttpResponse


def primeiro_teste(request):
    return HttpResponse("Olá, mundo!")


