from django.urls import path
from . import views
urlpatterns = [
    path("",views.home_page_view,name="home"),
    path("signin/",views.signin_page_view,name="signin"),
    path("signup/",views.signup_page_view,name="signup"),
    path("logout/",views.logout_user,name="logout"),
    path("subscribe/",views.subscribe_by_footer,name="subscribe"),
    path("panel/",views.customer_dashboard_view,name="dashboard"),
    path("controls/",views.admin_controller_view,name="controls"),
    path("developer/",views.developers_dashboard_view,name="developer"),
    path("news/",views.news_and_article_page_controller,name="articles"),
]
