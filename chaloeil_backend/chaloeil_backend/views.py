from django.shortcuts import render

def index(request):
    # Add your code here
    return render(request, 'index.html')