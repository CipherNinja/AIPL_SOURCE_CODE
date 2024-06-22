from django.shortcuts import render

# Create your views here.

def home_page_view(request):
    response = "Home Page Initial Setup"
    return render(
        request,
        "home_page/home_page.html",
        {"response":response}
    )

def signin_page_view(request):
    return render(
        request,
        "Signin_page/signin.html",
        {}
    )

def signup_page_view(request):
    return render(
        request,
        "Signup_page/signup.html",
        {}
    )