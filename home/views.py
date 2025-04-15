from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import ResearcherProfile, Research
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction, IntegrityError
import random
import string
import time
import re
from home.forms import userForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def index(request):
    latest_research = Research.objects.all().order_by('-publication_date')[:5]
    return render(request, "index.html", {'latest_research': latest_research})

def about(request):
    return render(request, "about.html")

@login_required(login_url='/login')
def profile(request):
    researcher, created = ResearcherProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'institution': 'Not Set',
            'department': 'Not Set',
            'qualification': 'Not Set',
            'research_field': 'Not Set'
        }
    )
    researches = Research.objects.filter(researcher=researcher)
    context = {
        'researcher': researcher,
        'researches': researches
    }
    return render(request, "profile.html", context)

@login_required(login_url='/login')
def upload_research(request):
    if request.method == "POST":
        researcher, created = ResearcherProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'institution': 'Not Set',
                'department': 'Not Set',
                'qualification': 'Not Set',
                'research_field': 'Not Set'
            }
        )
        
        research = Research(
            researcher=researcher,
            title=request.POST.get('title'),
            abstract=request.POST.get('abstract'),
            category=request.POST.get('category'),
            efficiency_percentage=request.POST.get('efficiency'),
            methodology=request.POST.get('methodology'),
            results=request.POST.get('results'),
            research_paper=request.FILES.get('research_paper')
        )
        research.save()
        messages.success(request, 'Research uploaded successfully!')
        return redirect('research_list')
    return render(request, "upload_research.html")
def research_list(request, category=None):
    sort_by = request.GET.get('sort', 'date')
    
    if category:
        researches = Research.objects.filter(category=category)
    else:
        researches = Research.objects.all()
        
    if sort_by == 'date':
        researches = researches.order_by('-publication_date')
    elif sort_by == 'efficiency':
        researches = researches.order_by('-efficiency_percentage')
        
    return render(request, "research_list.html", {'researches': researches})

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

@csrf_protect
def registerUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        country = request.POST.get('country')
        other_country = request.POST.get('other_country')
        academic_title = request.POST.get('academic_title')
        other_academic_title = request.POST.get('other_academic_title')
        # Validation checks

        final_country = other_country if country == 'other' else country
        final_academic_title = other_academic_title if academic_title == 'OTHER' else academic_title

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # Generate OTP
        otp = generate_otp()

        # Save user data in session
        request.session['user_data'] = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': pass1,
            'otp': otp,
            'country': final_country,
            'academic_title': final_academic_title,
        }

        # Send OTP to email
        if send_otp_email(email, otp):
            messages.success(request, "Registration successful! Please verify your email with the OTP sent.")
            return redirect('verify_email')

    return render(request, "register.html")


def verify_email(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        user_data = request.session.get('user_data')

        if not user_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        if otp == user_data.get('otp'):
            try:
                # Save the user to the database
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_active=True  # User is now active after verification
                )

                # Save the ResearcherProfile
                ResearcherProfile.objects.create(
                    user=user,
                    email_verified=True
                )

                # Clear session data
                del request.session['user_data']

                # Log the user in
                login(request, user)
                messages.success(request, "Email verified successfully!")
                return redirect('profile')
            except IntegrityError:
                messages.error(request, "User creation failed. Please try again.")
                return redirect('register')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_email.html")


def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        
        subject = f"New Contact Message from {name}"
        email_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Phone: {phone}

Message:
{desc}

Best regards,
Research Scholar Hub Team
"""
        
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
        
    return render(request, 'contact.html')


def privacy_policy(request):
    return render(request, 'privacy.html')

def research_detail(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    return render(request, 'research_detail.html', {'research': research})
def send_otp_email(email, otp):
    print(f"Sending OTP {otp} to {email}")  # Debug line
    try:
        send_mail(
            'Your OTP for Research Scholar Hub',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        print("Email sent successfully!")  # Debug line
        return True
    except Exception as e:
        print(f"Email sending details: {str(e)}")  # Debug line
        return False

def userForm(request):
    finalans=0
    
    fn=userForm()
    data={'form':fn}
    try:
        n1=int(request.POST.get('num1'))
        n2=int(request.POST.get('num2'))
        finalans = n1+n2
        data={'n1':n1,
              'n2':n2,
              'output':finalans,
              'form':fn}
        
    except:
        pass
    return render(request,'userform.html',data)