from django.urls import path
from django.contrib import admin
from . import views

admin.site.site_header = "Agratas Infotech Private Limited"

urlpatterns = [
    path("",views.home_page_view,name="home"),
    path("signin/",views.signin_page_view,name="signin"),
    path("signup/",views.signup_page_view,name="signup"),
    path("logout/",views.logout_user,name="logout"),
    path("subscribe/",views.subscribe_by_footer,name="subscribe"),
    path("panel/",views.customer_dashboard_view,name="dashboard"),
    path("developer/",views.developers_dashboard_view,name="developer"),
    path("articles/<str:page_name>/", views.news_and_article_page_controller, name="articles"),
    path("AgratAsiaHack/",views.AgratasiaHackView,name="AgratAsiaHack24"),
    path("privacy_and_policy/",views.privacy_static_render,name="privacy"),
    path("terms_and_conditions/",views.term_condition_static_render,name="t&c"),
    path("refund_policy/",views.refund_static_render,name="r&p"),
    path("internship/",views.internship_opportunity_page,name="internship"),
    path("maintenance/",views.maintenance_page_view,name="maintenance"),
    
]
