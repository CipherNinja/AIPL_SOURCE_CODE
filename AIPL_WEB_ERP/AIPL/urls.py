from django.urls import path
from django.contrib import admin
from . import views
from .views import SubscriberListView
admin.site.site_header = "Agratas Infotech Private Limited"

urlpatterns = [
    path("",views.home_page_view,name="home"),
    path("signin/",views.signin_page_view,name="signin"),
    path("signup/",views.signup_page_view,name="signup"),
    path("forget_password/",views.forget_password_view,name="forget_password"),
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
    path("education/<str:page_name>/",views.education_page_controller,name="education"),
    path("contact-agratas/",views.contact_agratas,name="contact_agratas"),
    path('administration/analytics/', views.analytics_view, name='analytics'),  # New analytics URL
    path('administration/analytics/send-alerts/', views.send_alerts, name='send_alerts'),
    path('api/subscribers/', SubscriberListView.as_view(), name='subscriber-list'),
    path("AIPL/<str:page_name>/",views.footer_links,name="f_connect"),
    
    
]
