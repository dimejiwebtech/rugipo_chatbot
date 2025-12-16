from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    context = {
        'page_title': 'Home'
    }
    return render(request, 'pages/home.html', context)

def about(request):
    context = {
        'page_title': 'About'
    }
    return render(request, 'pages/about.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # For now, just show success message
        # Later you can add email functionality or save to database
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    
    context = {
        'page_title': 'Contact Us'
    }
    return render(request, 'pages/contact.html', context)