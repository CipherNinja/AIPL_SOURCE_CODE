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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
                return redirect('dashboard')
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
        messages.error(request, "Please, SignIn to see this Content.")
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
        "banking":"banking_finance.html",
        "cloud":"cloudArticle.html",
        "cyber":"cybersecurity.html",
        "ecommerse":"Ecommerce.html",
        "overview":"overview.html",
        "our_impact":"impact.html",
        "testimonial":"testimonials.html",
        "leadership":"leadership.html",
        "webdevelopment":"web_development.html",
        "cybersecurity":"cybersecurity.html",
        "mobile-app-development":"mobile_app_development.html",
        "IT-Consultancy":"IT_consulting.html"
    
    }
    __link__ = __PAGES__.get(page_name, "common_page.html")
    
    # Ensure the correct template path
    return render(request, f"News&Articles/{__link__}")


def education_page_controller(request,page_name):
    
    __PAGES__ = {
        'faculty_development': "FDP.html",
        'industrial_training': "industrial_training.html",
        'placements': "placements.html",
        "techsummit":"techsummit.html",
    
    }
    __link__ = __PAGES__.get(page_name, "common_page.html")
    
    # Ensure the correct template path
    return render(request, f"Education/{__link__}")


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
    

def AgratasiaHackView(request):
    context = {"user": request.user}

    if request.method == "POST":
        # Extract team information
        team_name = request.POST.get('teamName')
        num_of_members = int(request.POST.get('numOfMembers', 0))

        # Extract leader information
        leader_name = request.POST.get('leaderName')
        leader_email = request.POST.get('leaderEmail')
        leader_phone = request.POST.get('leaderPhone')
        leader_linkedin = request.POST.get('leaderLinkedIn')
        leader_github = request.POST.get('leaderGithub')

        # Validate number of members
        if num_of_members < 1 or num_of_members > 4:
            messages.error(request, "Please select a valid number of team members (1-4).")
            return redirect('AgratAsiaHack24')

        # Check if the team name already exists
        if Team.objects.filter(team_name=team_name).exists():
            messages.error(request, "A team with this name already exists. Please choose a different team name.")
            return redirect('AgratAsiaHack24')

        # Create the team if the name is unique
        team = Team.objects.create(team_name=team_name)

        # Create the leader entry
        TeamMember.objects.create(
            team=team,
            is_leader=True,
            name=leader_name,
            email=leader_email,
            phone_number=leader_phone,
            linkedin_url=leader_linkedin,
            github_url=leader_github
        )

        # Add additional team members
        for i in range(1, num_of_members):
            member_name = request.POST.get(f'member{i}Name')
            member_email = request.POST.get(f'member{i}Email')
            member_phone = request.POST.get(f'member{i}Phone')
            member_linkedin = request.POST.get(f'member{i}LinkedIn')
            member_github = request.POST.get(f'member{i}Github')

            # Create a team member entry
            TeamMember.objects.create(
                team=team,
                is_leader=False,
                name=member_name,
                email=member_email,
                phone_number=member_phone,
                linkedin_url=member_linkedin,
                github_url=member_github
            )

        messages.success(request, "Team registered successfully!")
        return redirect('AgratAsiaHack24')

    return render(
        request,
        "Hackathon/AgratasiaHackForm.html",
        context
    )


def privacy_static_render(request):
    __JSON__ = {"user":request.user}
    return render(
        request,
        'base/privacy.html',
        __JSON__
    )

def refund_static_render(request):
    __JSON__ = {"user":request.user}
    return render(
        request,
        'base/refund2.html',
        __JSON__
    )

def term_condition_static_render(request):
    __JSON__ = {"user":request.user}
    return render(
        request,
        'base/Terms_and_Conditions.html',
        __JSON__
    )

def send_confirmation_email(application):
    # Define the subject and recipient
    subject = f"Application Confirmation for the {application.role} Position"
    recipient_email = application.email  # Assuming `application` object has `email` field

    # Render the HTML content using Django's template rendering
    html_content = render_to_string('Emails/internship_confirmation.html', {'application': application})
    text_content = strip_tags(html_content)  # Fallback for plain text version

    # Create the email message
    email = EmailMultiAlternatives(
        subject,
        text_content,
        'agratascommunity@gmail.com',  # From email
        [recipient_email]  # To email
    )
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()


def internship_opportunity_page(request):
    if request.method == 'POST':
        # Get the form data manually from POST
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        institute_name = request.POST.get('institute')
        course = request.POST.get('course')
        role = request.POST.get('role')
        branch = request.POST.get('branch')
        linkedin_profile_url = request.POST.get('linkedin')
        github_profile_url = request.POST.get('github')
        custom_resume = request.FILES.get('resume')
        college_id = request.POST.get('collegeId')

        # Check if an application with this email already exists
        if InternshipApplication.objects.filter(email=email).exists():
            messages.error(request, 'An application with this email address already exists. Please use a different email.')
            return render(request, 'Internship/internship.html')
        if InternshipApplication.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'An application with this phone number already exists. Please use a different phone no.')
            return render(request, 'Internship/internship.html')

        # Create the internship application instance without saving it yet
        application = InternshipApplication(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            institute_name=institute_name,
            course=course,
            role=role,
            branch=branch,
            linkedin_profile_url=linkedin_profile_url,
            github_profile_url=github_profile_url,
            custom_resume=custom_resume,
            college_id=college_id
        )

        # Validate the model instance (including file validators)
        try:
            application.full_clean()  # This will run all model validators including file size and extension
            application.save()  # If validation passes, save the application to the database
        except ValidationError as e:
            # If validation fails, capture the error and display it
            messages.error(request, e.message_dict)
            return render(request, 'Internship/internship.html')

        # Email confirmation message
        send_confirmation_email(application) # we are using UI as email
        
        
        # our_message = f"""
        #     Dear {application.first_name} {application.last_name},

        #     Thank you for your interest in the {application.role} position at Agratas Infotech.
        #     We have successfully received your application and resume, and we are excited to review your qualifications.
        #     ...
        #     Best regards,
        #     The Recruitment Team  
        #     Agratas Infotech Pvt. Ltd.
        # """

        # # Send confirmation email
        # send_mail(
        #     subject='Internship Application Confirmation',
        #     message=our_message,
        #     from_email='info@agratasinfotech.com',  # Replace with your actual email
        #     recipient_list=[application.email],
        #     fail_silently=False,
        # )

        # Redirect to a success page after saving
        messages.success(request, "Response Submitted, Check your Email Inbox 📧")
        return redirect('internship')

    return render(request, 'Internship/internship.html')

def maintenance_page_view(request):
    return render(
        request,
        "base/maintenance.html"
    )

