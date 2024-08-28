from django.db import models
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
        verbose_name = "Meeting Schedule"
        verbose_name_plural = "Meeting Schedule"


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


# We dont collect the other data only email for sending bussiness email
# this is the only Optimum way without creating the user
class subscribers(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

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

# Signal to send email after a news article is saved
@receiver(post_save, sender=newsArticle)
def send_mail_on_article_save(sender, instance, created, **kwargs):
    if created:  # Only send email when a new article is created
        instance.send_news_update()