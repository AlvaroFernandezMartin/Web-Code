from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from django.http import HttpResponse

import requests

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            message = form.cleaned_data['message']
            uploaded_file = form.cleaned_data['file']

            subject = f"[Contact Form] {name} from {company_name or 'N/A'}"
            message_body = f"""
Name: {name}
Company: {company_name}
Email: {email}
Telephone: {telephone}
Message: {message}
            """

            # Crear el mensaje
            email_message = EmailMessage(
                subject,
                message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
            )

            # Adjuntar el archivo si existe
            if uploaded_file:
                email_message.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

            # Enviar el email
            email_message.send(fail_silently=False)

            return render(request, 'index.html')  # o redirigir a página de gracias

    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})


def test_email(request):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "Bensons Website","email": "89f19d001@smtp-brevo.com"},
        "to": [{"email": "alvarofernandezmartintr@gmail.com", "name": "Alvaro"}],
        "subject": "Test Email via Brevo API",
        "htmlContent": "<html><body><h1>Hello from Brevo API!</h1><p>This is a test email sent from Django using Brevo API.</p></body></html>"
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)
    print(response.text)  # <--- Añade esto para ver la respuesta completa

    if response.status_code == 201:
        return HttpResponse("✅ Email sent successfully via Brevo API.")
    else:
        return HttpResponse(f"❌ Failed to send email: {response.status_code}\n{response.text}")



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

def brochures(request):
    return render(request, 'brochures.html')  


# def contact_us(request):
#     return render(request, 'contact_us.html')


