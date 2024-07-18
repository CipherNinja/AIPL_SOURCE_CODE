from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
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
            return redirect('home')
    
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
def dashboard_panel_view(request):
    if request.user.is_authenticated:
        return render(
            request,
            "customer_dashboard/customer_panel.html"
        )
    else:
        messages.success(request,"you are not authorised to see this content")
        return redirect("home")