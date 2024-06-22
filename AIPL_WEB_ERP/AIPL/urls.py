from django.urls import path
from . import views
urlpatterns = [
    path("",views.home_page_view,name="home"),
    path("signin/",views.signin_page_view,name="signin"),
    path("signup/",views.signup_page_view,name="signup"),
]
