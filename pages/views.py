from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from django.http import HttpResponse

import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('telephone')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('file')

        # Guardar el archivo temporalmente (si existe)
        file_url = ""
        if uploaded_file:
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "File size exceeds 5MB.")
                return redirect('pages:contact_us')
            file_path = default_storage.save(f"temp/{uploaded_file.name}", ContentFile(uploaded_file.read()))
            file_url = request.build_absolute_uri(default_storage.url(file_path))

        # Configuración de la API de Brevo
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Preparar contenido del correo
        html_content = f"""
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Company:</strong> {company}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Message:</strong><br>{message}</p>
        """
        if file_url:
            html_content += f'<p><strong>File Uploaded:</strong> <a href="{file_url}">{uploaded_file.name}</a></p>'

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "dialga602002@gmail.com"}],
            sender={"name": name, "email": email},
            subject=f"New contact from {name} via Bensons Workwear",
            html_content=html_content
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            messages.success(request, "Your message has been sent successfully.")
        except ApiException as e:
            messages.error(request, f"Failed to send message. {e}")

        return redirect('pages:contact_us')

    return render(request, 'contact_us.html')



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


