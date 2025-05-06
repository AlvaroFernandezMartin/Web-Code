from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Category


import os

@csrf_exempt  

def home(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'products': products, 'categories': categories})

def clothing_catalogue(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    return render(request, 'clothing_catalogue.html', {'products': products, 'categories': categories})


def case_study(request):
    return render(request, 'case_study.html')  

def about_us(request):
    return render(request, 'about_us.html')  

def faq(request):
    return render(request, 'faq.html')  

def brochures(request):
    return render(request, 'brochures.html')  

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('telephone')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('file')

        # Validate max file size (5 MB)
        if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:
            messages.error(request, "The file exceeds the maximum allowed size of 5 MB.")
            return redirect('pages:contact_us')

        # Validate allowed file types
        if uploaded_file:
            ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.txt', '.eps', '.ai']
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                messages.error(request, "Unsupported file type.")
                return redirect('pages:contact_us')

        # Message content
        subject = f"New message from the contact form: {name}"
        body = f"""
                    Name: {name}
                    Company: {company}
                    Email: {email}
                    Phone: {phone}

                    Message:
                    {message}
                """

        # Send email via SMTP (Brevo)
        email_msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[email]
        )

        if uploaded_file:
            email_msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

        try:
            email_msg.send(fail_silently=False)
            messages.success(request, "Your message has been sent successfully.")
        except Exception as e:
            messages.error(request, f"Failed to send the message: {e}")

        return redirect('pages:contact_us')

    return render(request, 'contact_us.html')

