from django.shortcuts import render
from django.http import HttpResponse

# Create your views here. [endpoints: a location on the web that you are going to (think of a webpage)]



def main(request):
    return HttpResponse("<h1>Hello, World!</h1>")
