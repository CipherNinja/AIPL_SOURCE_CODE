from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
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
            messages.success(request,f" Welcome back {uname}")
            return redirect('dashboard')
        else:
            messages.error(request," Wrong Credentials !")
            return redirect('signin')
    
    return render(
        request,
        "Signin_page/signin.html",
        {}
    )

def signup_page_view(request):
    if request.method == "POST":
        username = request.POST["set_username"]
        email_id = request.POST["set_email"] 
        set_password = request.POST["set_password"]
        cnf_password = request.POST["cnf_password"]
        try:
            if len(username) < 6:
                messages.success(request,f"Username is too short")
                redirect("signup")
            if set_password != cnf_password:
                messages.success(request,"Create password and Confirm password must be same")
                redirect("signup")
            elif len(set_password)<8:
                messages.success(request,"Password is too short try with minimum 8 characters")
                redirect("signup")
            # elif set_password.isalnum() == False:
            #     messages.success(request,"Password must be Alpha Numeric")
            #     redirect("signup")
            elif User.objects.filter(username=username):
                messages.success(request,f"{username} is not available as username")
                redirect("signup")
            elif User.objects.filter(email=email_id):
                messages.success(request,f"A username already exist on your email")
                redirect("signup")
            else:
                newuser = User.objects.create_user(username=username,email=email_id,password=cnf_password)
                newuser.save()
                myuser = authenticate(request,username=username,password=set_password)
                login(request,myuser)
                messages.success(request,f"Welcome {myuser.get_username()}, Thanks for joining us 🙏")
                return redirect("dashboard")
        except Exception as e:
            print(e)
        
        pass
    return render(
        request,
        "Signup_page/signup.html",
        {}
    )

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

        return render(
            request,
            "customer_dashboard/customer_panel.html"
        )
    else:
        messages.error(request, "You are not authorized to see this content.")
        return redirect("home")
