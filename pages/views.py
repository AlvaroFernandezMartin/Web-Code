from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from .forms import ContactForm

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener los datos del formulario
            name = form.cleaned_data['name']
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            message = form.cleaned_data['message']
            file = form.cleaned_data['file']

            # Crear el contenido del correo
            subject = f"New Contact Form Submission from {name}"
            message_body = f"""
                Name: {name}
                Company: {company_name}
                Email: {email}
                Telephone: {telephone}
                Message: {message}
            """
            
            # Enviar el correo
            send_mail(
                subject,
                message_body,
                email,  # El correo de la persona que llena el formulario
                [settings.CONTACT_EMAIL],  # Correo al que se enviará el mensaje
                fail_silently=False,
            )

            # Redirigir a una página de agradecimiento
            return render(request, 'thank_you.html')
    
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})


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


def contact_us(request):
    return render(request, 'contact_us.html')