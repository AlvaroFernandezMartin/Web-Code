from django.shortcuts import render

def home(request):
    return render(request, 'index.html') 

def clothing_catalogue(request):
    return render(request, 'clothing_catalogue.html')  
