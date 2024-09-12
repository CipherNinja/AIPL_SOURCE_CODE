from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
import re
from .models import *
# Create your views here.

def home_page_view(request):
    response = "Home Page Initial Setup"
    return render(
        request,
        "home_page/home_page.html",
        {"response":response}
    )

def signin_page_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            uname = user.get_username()
            login(request,user)
            # Check if the user has staff status
            if user.is_staff:
                return redirect("developer")
            else:
                messages.success(request,f" Welcome back {uname}")
                return redirect('developer')
        else:
            messages.error(request," Wrong Credentials !")
            return redirect('signin')
    
    return render(
        request,
        "Signin_page/signin.html",
        {}
    )

def validate_username(username):
    # Allow only alphanumeric characters and underscores
    if not re.match(r'^[\w]+$', username):
        raise ValidationError(_('Username contains invalid characters'))

def validate_password(password):
    # Minimum 8 characters, at least 1 letter and 1 number
    if len(password) < 8:
        raise ValidationError(_('Password must be at least 8 characters long'))
    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        raise ValidationError(_('Password must contain both letters and numbers'))

def signup_page_view(request):
    if request.method == "POST":
        username = request.POST.get("set_username")
        email_id = request.POST.get("set_email")
        set_password = request.POST.get("set_password")
        cnf_password = request.POST.get("cnf_password")

        try:
            # Validate username
            if not isinstance(username, str):
                raise ValidationError("Invalid username format.")
            if not isinstance(email_id, str):
                raise ValidationError("Invalid email format.")

            # Validate password match
            if set_password != cnf_password:
                messages.error(request, "Create password and Confirm password must be the same")
                return redirect("signup")
            
            # Validate password (Django's validate_password will handle string checks)
            validate_password(set_password)
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' is not available")
                return redirect("signup")
            
            if User.objects.filter(email=email_id).exists():
                messages.error(request, f"An account with this email already exists")
                return redirect("signup")
            
            # Create new user
            newuser = User.objects.create_user(username=username, email=email_id, password=set_password)
            newuser.save()
            
            # Authenticate and log in user
            myuser = authenticate(request, username=username, password=set_password)
            if myuser is not None:
                login(request, myuser)
                messages.success(request, f"Welcome {myuser.get_username()}, Thanks for joining us 🙏")
                return redirect("dashboard")
            else:
                messages.error(request, "Authentication failed")
                return redirect("signup")
        
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("signup")
        except Exception as e:
            messages.error(request, "An error occurred. Please try again later.")
            print(e)  # This will help you track the exact exception
            return redirect("signup")
    
    return render(request, "Signup_page/signup.html", {})

def logout_user(request):
    logout(request)
    messages.success(request," Logged out ")
    return redirect("home")

# CUTOMER DASHBOARD
def customer_dashboard_view(request):
    # If user is authenticated then he will be redirected to the customer dashboard
    if request.user.is_authenticated:
        # If user is making POST request on dashboard
        if request.method == "POST":
            """
            user can make two types of post request 
            1. request for data deletion
            2. request for meeting with agratas

            """
            # handling data deletion requests
            if 'deletionReason' in request.POST:
                deletion_reason = request.POST.get("deletionReason")
                additional_details = request.POST.get("additionalDetails")

                try:
                    # Check if the user has submitted any requests before
                    last_request = dataDeletionModel.objects.filter(user=request.user).order_by('-timestamp').first()

                    if last_request:
                        # If a request exists, check the time since the last submission
                        time_since_last_request = timezone.now() - last_request.timestamp
                        if time_since_last_request < timedelta(hours=24):
                            messages.error(request, "You can only submit a request once every 24 hours.")
                            return redirect('dashboard')

                    # Create the deletion request if no recent request was made
                    dataDeletionModel.objects.create(
                        user=request.user,
                        reason=deletion_reason,
                        additional_info=additional_details
                    )
                    messages.success(request, "Your Response has been registered! Check your email.")
                except Exception as e:
                    messages.error(request, "An error occurred while processing your request. Please try again later.")
                    # Optionally log the exception
                    print(f"Error processing deletion request: {e}")

            
            # Checking if meeting form is filled and submitted a POST request
            # Key Considerations -
            # 1. User can select the time zone (UTC/IST,etc) as per his convinience
            # 2. Any international time zone must be converted into Indian Standard Time Zone
            # 3. Meeting form filled once within 24 Hrs.
            
            elif "date" in request.POST:
                date = request.POST.get("date")
                time = request.POST.get("time")
                tz = request.POST.get("timezone")
                location = request.POST.get("location")
                reason = request.POST.get("reason")
                description = request.POST.get("description")
                try:
                    # Check if the user has submitted any requests before
                    last_request = Meeting.objects.filter(user=request.user).order_by('-created_at').first()

                    if last_request:
                        # If a request exists, check the time since the last submission
                        time_since_last_request = timezone.now() - last_request.created_at
                        if time_since_last_request < timedelta(hours=24):
                            messages.error(request, "You can only submit a request once every 24 hours.")
                            return redirect('dashboard')

                    # timezone conversion to IST

                    anyTimeZoneWorld = ZoneInfo(tz)
                    istTimeZone = ZoneInfo("Asia/Kolkata")
                    today = datetime.now().date()
                    anyTimeZone = datetime.strptime(f'{today} {time+":00"}',"%Y-%m-%d %H:%M:%S")
                    anyTimeZone = anyTimeZone.replace(tzinfo=anyTimeZoneWorld)
                    istTime = anyTimeZone.astimezone(istTimeZone)
                    istTimeTime,istTimeDate = istTime.strftime("%H:%M:%S"),istTime.strftime("%Y-%m-%d")
                    
                    Meeting.objects.create(
                        user=request.user,date=istTimeDate,
                        time=istTimeTime,timezone=tz,
                        location=location,reason=reason,
                        description=description
                    )
                    messages.success(request,f"We recieved your meeting schedule")
                except Exception as e:
                    messages.error(request, "An error occurred while processing your request. Please try again later.")
                    # Optionally log the exception
                    print(f"Error processing Meeting request: {e}")
        try:
            notifications = Notification.objects.filter(recipient=request.user)
        except Notification.DoesNotExist as e:
            pass
        return render(
            request,
            "customer_dashboard/customer_panel.html",
            {'notifications': notifications},
        )
    else:
        messages.error(request, "You are not authorized to see this content.")
        return redirect("home")

def subscribe_by_footer(request):
    if request.method == "POST":
        try:
            email_id = request.POST.get("subscribe")
            if subscribers.objects.filter(email=email_id).exists():
                messages.error(request, "Email already exists!")
            else:
                subscribers.objects.create(email=email_id).save()
                messages.success(request, "You have Subscribed to Agratas Infotech, Successfully!")
        except subscribers.DoesNotExist as e:
            pass
        # Redirect to the current page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def news_and_article_page_controller(request,page_name):
    
    __PAGES__ = {
        'artificialintelligence': "ArtificialIntelIigence.html",
        'digitalmarketing': "DigitalMarketing.html",
        'internetofthings': "InternetOfThings.html",
        # Add more pages here
    }
    __link__ = __PAGES__.get(page_name, "common_page.html")
    
    # Ensure the correct template path
    return render(request, f"News&Articles/{__link__}")



def developers_dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(
                request,
                "developer_dashboard/Dev_dashboard.html"
            )
        else:
            messages.error(request, "You do not have the necessary permissions to access this page.")
            return redirect('home')  # Redirect to a different page if the user is not a staff member
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('signin')  # Redirect to signin page if the user is not authenticated