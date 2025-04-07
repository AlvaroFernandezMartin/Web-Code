from django.shortcuts import render

def home(request):
    return render(request, 'index.html') 

def clothing_catalogue(request):
    return render(request, 'clothing_cathalogue.html')  

def case_study(request):
    return render(request, 'case_study.html')  

def about_us(request):
    return render(request, 'about_us.html')  

def faq(request):
    return render(request, 'faq.html')  