from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .utils import get_chart


# Create your views here. [endpoints: a location on the web that you are going to (think of a webpage)]

def main(request):
    # return HttpResponse("<h1>Hello, World!</h1>")

    chart = None

    chart = get_chart()
    name = 'BanklessDAO'

    context = {
        'chart': chart,
        'name': name
    }


    return render(request, 'bb.html', context)
