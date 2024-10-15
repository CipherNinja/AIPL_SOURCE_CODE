from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save 
from django.dispatch import receiver
# import pytz

# Create your models here.

class dataDeletionModel(models.Model):
    choice_for_deletion = [
    ('privacy concern','Privacy Concern'),
    ('security concern','Security Concern'),
    ('no longer needed','No Longer Needed'),
    ('regulatory request (e.g. gdpr/ccpa)','Regulatory Request (e.g. GDPR/CCPA)'),
    ('other','Other'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.CharField(choices=choice_for_deletion,max_length=55)
    additional_info = models.TextField(max_length=1500)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        verbose_name = "Data Deletion Request"
        verbose_name_plural = "Data Deletion Requests"


# Same model will be used if we want to set meeting with developer, HR etc
class Meeting(models.Model):
    REASON_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Support', 'Support'),
        ('Demo', 'Demo'),
        ('Product Demonstration', 'Product Demonstration'),
        ('Business Development', 'Business Development'),
        ('Strategic Planning', 'Strategic Planning'),
        ('Project Kickoff', 'Project Kickoff'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateField()  # Date of the meeting
    time = models.TimeField()  # Time of the meeting
    timezone = models.CharField(max_length=100, default='UTC')  # Time zone of the meeting
    location = models.CharField(max_length=255)  # Location of the meeting
    reason = models.CharField(choices=REASON_CHOICES, max_length=50)  # Reason for the meeting
    description = models.TextField()  # Additional details about the meeting
    created_at = models.DateTimeField(auto_now_add=True)  # When the meeting was scheduled

    def __str__(self):
        return f"Meeting on {self.date} at {self.time} with {self.user.username}"

    class Meta:
        ordering = ['date', 'time']
        verbose_name = "Available Meeting"
        verbose_name_plural = "Available Meeting"


'''
WE ARE USING SAME MODEL FOR CUSTOMER VIEW,DEVELOPER VIEW (Global)
FOR SENDING RESPONSE AS A NOTIFICATION
[.] FUTURE UPDATE (PENDING): Integrate the model with smtp protocol and send the notification
                                on Email of customer/staff.
'''
# model for sending the notification to the customer/staff
class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ManyToManyField(User, related_name='received_notifications',)
    message = models.TextField()
    meeting_link = models.URLField(blank=True, null=True)  # Optional field
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # we can use a cross/cancel button with GET method to set is_read = False | (hide or delete the notification)

    def __str__(self):
        recipient_names = ", ".join(user.username for user in self.recipient.all())
        return f'Notification from {self.sender.username} to {recipient_names} at {self.timestamp}'

    def get_recipient_names(self):
        return ", ".join(user.username for user in self.recipient.all())
    
    class Meta:
        verbose_name = "Notify/Update Sender "
        verbose_name_plural = "Notify/Update Sender "


# We dont collect the other data only email for sending bussiness email
# this is the only Optimum way without creating the user
class subscribers(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "View Subscriber's Email "
        verbose_name_plural = "View Subscriber's Email "


class newsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Automatically sends the message if any news article is saved
    def send_news_update(self):
        subscriber = subscribers.objects.all()  # Fetch all subscribers
        print(subscribers)
        recipient_list = [subscriber.email for subscriber in subscriber]  # Corrected variable name

        subject = f"News Update: {self.title}"
        message = f"{self.title}\n\n{self.content}"

        send_mail(
            subject=subject,
            message=message,
            from_email="droppersconnect@gmail.com",
            recipient_list=recipient_list,
            fail_silently=False,
        )
    class Meta:
        verbose_name = "Email Sender (Limited to Subscribers) "
        verbose_name_plural = "Email Sender (Limited to Subscribers) "

# Signal to send email after a news article is saved
@receiver(post_save, sender=newsArticle)
def send_mail_on_article_save(sender, instance, created, **kwargs):
    if created:  # Only send email when a new article is created
        instance.send_news_update()


class developer_profile(models.Model):
    developer_role = [
        ('Frontend Dev', "Frontend Dev"),
        ('Backend Dev', "Backend Dev"),
        ('DevOps Eng', "DevOps Eng"),
        ('Fullstack Dev', "Fullstack Dev"),
        ('IOS Dev', "IOS Dev"),
        ('Software Dev', "Software Dev"),
        ("AI/ML Eng", "AI/ML Eng"),
        ("Data Analyst", "Data Analyst"),
        ("DB Admin", "DB Admin"),
        ("Cloud Dev", "Cloud Dev"),
        ("Blockchain Dev", "Blockchain Dev"),
        ("AR/VR Dev", "AR/VR Dev"),
        ("Test Automation", "Test Automation"),
        ("BDA Trainee", "BDA Trainee"),
        ('Content Writer', "Content Writer"),
        ("Digital Marketing Trainee", "Digital Marketing Trainee"),
        ("Backend Dev .Net", "Backend Dev .Net"),
        ("Backend Dev PHP", "Backend Dev PHP"),
        ("Database Administrator", "Database Administrator"),
        ("SDE with Java", "SDE with Java"),
        ("Business Development Analyst", "Business Development Analyst")
    ]
    developer = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="Employee ID")
    job_role = models.CharField(choices=developer_role,max_length=50)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.developer.first_name} {self.developer.last_name} | {self.job_role}"
    
    class Meta:
        verbose_name = "AIPL's Employee "
        verbose_name_plural = "AIPL's Employee "

class AddTaskDetail(models.Model):
    title = models.CharField(max_length=80)
    detail = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now=True)
    accepted_by = models.OneToOneField(User,on_delete=models.CASCADE,default=1)


    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Task Assign Tool "
        verbose_name_plural = "Task Assign Tool "
    

from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    is_leader = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    institution = models.CharField(max_length=50,blank=True)
    institution_id = models.CharField(max_length=50,blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 1024:  # 1 MB limit
        raise ValidationError("The maximum file size that can be uploaded is 1MB")
    return value

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed")
    return value

class InternshipApplication(models.Model):
    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Enforces email uniqueness at the database level
    phone_number = models.CharField(max_length=15)
    
    # Educational Info
    institute_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    role = models.CharField(max_length=100, choices=[
        # Development Roles
        ('Machine Learning Intern', 'Machine Learning with Python'),
        ('Artificial Intelligence Intern', 'Artificial Intelligence and GenAI'),
        ('Cyber Security Intern', 'Cyber Security Analyst'),
        ('Full Stack Development Intern', 'Full Stack Web Development (MERN Stack)'),
        ('Android Development Intern', 'Android Development'),
        ('Data Analyst Intern', 'Data Science with PYTHON'),
        ('Cloud Computing Intern', 'Cloud Computing'),
        ('IOS App Development Intern', 'IOS App Development'),
        ('Dot Net Backend Development Intern', 'Backend with .Net'),
        ('PHP Backend Development Intern', 'Backend with PHP'),
        ('Database Admin Intern', 'Database Administrator'),
        ('SDE with Java Trainee', 'SDE with Java'),
        ('UIUX Development Intern', 'UI UX Developer Intern'),

        # Management/Non-Development Roles
        ('Digital Marketing Intern', 'Digital Marketing'),
        ('Content Writer Intern', 'Content Writer'),
        ('Finance Intern', 'Finance'),
        ('Marketing Intern', 'Marketing'),
        ('Business Development Analyst Intern', 'Business Development Analyst')
    ])


    branch = models.CharField(
        max_length=100,
        choices=[
            ('cse', 'Computer Science'),
            ('ee', 'Electrical Engineering'),
            ('me', 'Mechanical Engineering'),
            ('ce', 'Civil Engineering'),
            ('it', 'Information Technology'),
            ('ece', 'Electronics and Communication Engineering'),
            ('mse', 'Materials Science and Engineering'),
            ('env', 'Environmental Engineering'),
            ('automobile', 'Automobile Engineering'),
            ('hr', 'Human Resources'),
            ('finance', 'Finance'),
            ('marketing', 'Marketing'),
            ('business_admin', 'Business Administration'),
            ('digital_marketing', 'Digital Marketing'),
        ]
    )

    
    # Profile URLs
    linkedin_profile_url = models.URLField(blank=True, null=True)
    github_profile_url = models.URLField(blank=True, null=True)
    
    # Resume Upload (with validation for PDF format and size limit)
    custom_resume = models.FileField(
        upload_to='nginx/resumes/', 
        blank=True, 
        null=True,
        validators=[validate_file_size, validate_file_extension]
    )
    
    # College ID
    college_id = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role}'
