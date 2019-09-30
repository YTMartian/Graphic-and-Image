from django.shortcuts import render


def index(request):
    return render(request, 'system/index.html')


def print_(request):
    return render(request, 'system/print.html')