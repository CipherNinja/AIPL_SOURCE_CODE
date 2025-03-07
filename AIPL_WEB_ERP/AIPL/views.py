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
from django.contrib.auth.hashers import make_password

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
        "IT-Consultancy":"IT_consulting.html",
        "research-and-development":"R&D.html"
    
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
        'erp@agratasinfotech.com',  # From email
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


import random

# Function to send the OTP email
def send_otp_email(email, otp_code):
    # Define the subject and recipient
    subject = "Your OTP for Password Reset"
    recipient_email = email

    # Render the HTML content using Django's template rendering
    html_content = render_to_string('Emails/Otp_Template.html', {'otp_code': otp_code})
    text_content = strip_tags(html_content)  # Fallback for plain text version

    # Create the email message
    email_message = EmailMultiAlternatives(
        subject,
        text_content,
        'erp@agratasinfotech.com',  # From email
        [recipient_email]  # To email
    )
    email_message.attach_alternative(html_content, "text/html")

    # Send the email
    email_message.send()


def forget_password_view(request):
    if request.method == "POST":
        # Reset Password Submission
        if 'new_password' in request.POST and 'confirm_password' in request.POST:
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            email = request.session.get("email")
            
            if not email:
                messages.error(request, "Session expired. Please start the process again.")
                return redirect("forget_password")
            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match. Please try again.")
                return render(request, "Forget_Pass/reset_password.html")
            
            # Update the password for the associated user
            try:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                del request.session['email']  # Clear email from session
                messages.success(request, "Password has been reset successfully. You can now log in.")
                return redirect("signin")  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
                return redirect("forget_password")

        # OTP Verification
        elif 'otp1' in request.POST and 'otp2' in request.POST and 'otp3' in request.POST and 'otp4' in request.POST:
            otp_entered = request.POST.get("otp1") + request.POST.get("otp2") + request.POST.get("otp3") + request.POST.get("otp4")
            otp_saved = request.session.get("otp")
            email = request.session.get("email")
            
            if otp_saved and otp_entered == otp_saved:
                del request.session['otp']
                messages.success(request, "OTP verified. You can now reset your password.")
                return render(request, "Forget_Pass/reset_password.html")  # Show password reset form
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return render(request, "Forget_Pass/otp_verify.html")

        # Email Submission
        elif 'email' in request.POST:
            email = request.POST.get("email")
            if not User.objects.filter(email=email).exists():
                messages.error(request, "No user is associated with this email.")
                return redirect("forget_password")

            otp = str(random.randint(1000, 9999))
            request.session['otp'] = otp
            request.session['email'] = email
            
            send_otp_email(email, otp)
            messages.info(request, "OTP has been sent to your email.")
            return render(request, "Forget_Pass/otp_verify.html")

    return render(request, "Forget_Pass/forget_pass.html")



def contact_agratas(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email_id")
        phone = request.POST.get("phone_number")
        messages = request.POST.get("message")
        subject = request.POST.get("subject")

        # Get sender details from user input
        sender_role = request.POST.get("sender_role", "Support Staff")
        sender_email = request.POST.get("sender_email", email)  # Use user's email if sender_email not provided
        
        # Email recipients
        recipient_list = ["priyesh.pandey@agratasinfotech.com", "sandip.singh@agratasinfotech.com"]
        
        # Render the HTML content using the updated template
        html_content = render_to_string('Emails/contact_us_template.html', {
            'sender': full_name,
            'sender_email': sender_email,
            'phone': phone,
            'sender_role': sender_role,
            'subject': subject,
            'message': messages,
            'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        
        text_content = strip_tags(html_content)  # Fallback for plain text version
        
        # Create the email
        email_message = EmailMultiAlternatives(
            subject=f"New Contact Message: {subject}",
            body=text_content,  # Plain-text version
            from_email="erp@agratasinfotech.com",
            to=recipient_list,
        )
        email_message.attach_alternative(html_content, "text/html")  # Attach the HTML version
        
        # Send the email
        email_message.send()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def custom_404_view(request, exception):
    return render(request, 'Error/404_Not_Found.html', status=404)

def custom_500_view(request):
    return render(request, 'Error/500.html', status=500)

def custom_403_view(request, exception):
    return render(request, 'Error/403.html', status=403)

def custom_400_view(request, exception):
    return render(request, 'Error/400_Bad_Request.html', status=400)

from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from datetime import timedelta

@staff_member_required
def analytics_view(request):
    # Fetch all tasks with related user information
    tasks = ManageTask.objects.select_related('task_sender', 'receiver').values(
        'task_created_at', 'task_completion_status', 'task_deadline', 
        'task_priority', 'task_progress', 'task_sender__username', 
        'receiver__username', 'receiver__first_name'
    )
    df = pd.DataFrame(tasks)
    
    # Handle empty DataFrame case
    if df.empty:
        return render(request, 'admin/analytics.html', {
            'completion_rate': 0,
            'priority_efficiency': {},
            'overdue_tasks_count': 0,
            'overdue_tasks_details': [],
            'task_volume': {},
            'user_performance': {},
            'completion_times': [],
            'user_task_counts': {}
        })

    # Convert date fields to datetime
    df['task_created_at'] = pd.to_datetime(df['task_created_at'])
    df['task_deadline'] = pd.to_datetime(df['task_deadline'])
    
    # 1. Completion Rate
    completion_rate = df['task_completion_status'].mean() * 100

    # 2. Completion Efficiency by Priority
    df['completion_time'] = (df['task_deadline'] - df['task_created_at']).dt.days
    priority_efficiency = df[df['task_completion_status']].groupby('task_priority')['completion_time'].mean().to_dict()

    # 3. Overdue Tasks Count and Details
    now = timezone.now()
    overdue_tasks_df = df[
        (df['task_completion_status'] == False) &
        (df['task_deadline'] < now) &
        (df['task_progress'] != 'dismantel')  # Exclude dismantel tasks from email consideration
    ]

    # Include dismantel tasks separately
    dismantel_tasks_df = df[
        (df['task_completion_status'] == False) &
        (df['task_deadline'] < now) &
        (df['task_progress'] == 'dismantel')  # Include dismantel tasks in overdue
    ]

    # Combine overdue tasks and dismantel tasks
    all_overdue_tasks_df = pd.concat([overdue_tasks_df, dismantel_tasks_df])
    overdue_tasks_count = len(all_overdue_tasks_df)

    # Prepare details for rendering
    overdue_tasks_details = all_overdue_tasks_df[
        ['task_sender__username', 'receiver__username', 'task_priority', 'task_deadline', 'task_created_at']
    ].to_dict(orient='records')

    # 4. Task Volume by Priority and Status
    task_volume_raw = pd.crosstab(df['task_progress'], df['task_priority']).to_dict()

    priorities = ['high', 'medium', 'low']
    statuses = ['not started', 'in progress', 'completed']

    task_volume_transformed = {
        'labels': priorities,
        'datasets': []
    }

    for status in statuses:
        data = [task_volume_raw.get(status, {}).get(priority, 0) for priority in priorities]
        task_volume_transformed['datasets'].append({
            'label': status.capitalize(),
            'data': data,
            'backgroundColor': {
                'not started': '#FFC107',
                'in progress': '#03A9F4',
                'completed': '#4CAF50'
            }.get(status, '#000000')
        })

    # 5. User Performance with additional details, including absolute average completion time
    user_performance_df = df.groupby(['receiver__username', 'receiver__first_name']).agg(
        total_tasks=('task_completion_status', 'count'),
        completed_tasks=('task_completion_status', 'sum'),
        avg_completion_time=('completion_time', 'mean')
    ).reset_index()
    
    user_performance_df['abs_avg_completion_time'] = user_performance_df['avg_completion_time'].abs()
    user_performance = user_performance_df.set_index('receiver__username').T.to_dict()

    # 6. Completion Times for Line Chart
    df['completion_time_relative'] = (df['task_deadline'] - df['task_created_at']).dt.days
    completion_times = {
        'labels': df['task_created_at'].dt.strftime('%Y-%m-%d').tolist(),
        'data': df['completion_time_relative'].tolist()
    }

    # 7. Tasks Assigned vs. Tasks Completed per User
    task_counts = df.groupby('receiver__username').agg(
        tasks_assigned=('task_completion_status', 'count'),
        tasks_completed=('task_completion_status', 'sum')
    ).reset_index()
    
    user_task_counts = {
        'labels': task_counts['receiver__username'].tolist(),
        'tasks_assigned': task_counts['tasks_assigned'].tolist(),
        'tasks_completed': task_counts['tasks_completed'].tolist()
    }

    context = {
        'completion_rate': completion_rate,
        'priority_efficiency': priority_efficiency,
        'overdue_tasks_count': overdue_tasks_count,
        'overdue_tasks_details': overdue_tasks_details,
        'task_volume': task_volume_transformed,
        'user_performance': user_performance,
        'completion_times': completion_times,
        'user_task_counts': user_task_counts
    }

    return render(request, 'admin/analytics.html', context)


def footer_links(request,page_name):

    __PAGES__ = {
        'aboutus': "AboutUs/aboutus.html",
        'contactus': "contactus/contactus.html",
    }
    __link__ = __PAGES__.get(page_name, "base/maintenance.html")
    
    # Ensure the correct template path
    return render(request, __link__)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import subscribers
from .serializers import SubscriberSerializer

class SubscriberListView(APIView):
    def get(self, request):
        subscribers_data = subscribers.objects.all()
        serializer = SubscriberSerializer(subscribers_data, many=True)
        return Response(serializer.data)
    


from django.http import JsonResponse
from django.utils.timezone import now

@staff_member_required
def send_alerts(request):
    if request.method == "POST":
        # Fetch overdue tasks
        overdue_tasks = ManageTask.objects.filter(
            task_completion_status=False,
            task_deadline__lt=now()
        )

        # Loop through overdue tasks and send email alerts
        for task in overdue_tasks:
            try:
                # Prepare email context
                email_context = {
                    'receiver_name': task.receiver.first_name,
                    'task_title': task.task_title,
                    'task_detail': task.task_detail,
                    'task_deadline': task.task_deadline.strftime('%Y-%m-%d %H:%M:%S'),
                    'task_priority': task.task_priority.capitalize(),
                    'task_sender': task.task_sender.username if task.task_sender else "Admin",
                    'warning_message': (
                        "Failing to complete this task will result in a loss of credit points and a lower rank. "
                        "Lower-ranking developers may be replaced, while higher-ranking developers enjoy more perks "
                        "and authority. Please act on this task immediately to avoid penalties."
                    ),
                }

                # Render email template
                html_content = render_to_string('Emails/overdue_task.html', email_context)

                # Send email
                email = EmailMultiAlternatives(
                    subject=f"Overdue Task Alert: {task.task_title}",
                    body="Your task is overdue. Please check your account for details.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[task.receiver.email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

            except Exception as e:
                print(f"Error sending email for task {task.task_title}: {e}")

        # Return success response
        return JsonResponse({"success": True})

    # If request is not POST, return failure response
    return JsonResponse({"success": False})
