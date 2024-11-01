from django.contrib import admin
from django import forms
from .models import *
# Register your models here.


@admin.register(dataDeletionModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","reason","additional_info","timestamp"]

@admin.register(Meeting)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","date","time","location","reason","description"]


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'get_recipient_names', 'message', 'timestamp', 'is_read')
    
    exclude = ('sender',)  # Exclude the sender field from the admin form

    def get_recipient_names(self, obj):
        return obj.get_recipient_names()
    get_recipient_names.short_description = 'Recipients'
    
    def save_model(self, request, obj, form, change):
        # Automatically assign the sender as the currently logged-in user
        if not obj.sender:
            obj.sender = request.user
        obj.save()

# Register the admin class
admin.site.register(Notification, NotificationAdmin)


admin.site.register(subscribers)
admin.site.register(newsArticle)

@admin.register(developer_profile)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","developer","job_role","points","rank"]
    ordering = ["rank"]

# Custom form to restrict editing for non-superuser staff
class ManageTaskAdminForm(forms.ModelForm):
    class Meta:
        model = ManageTask
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if we are editing an existing task (obj is not None)
        if self.instance and self.instance.pk:
            # Disable fields for non-superuser staff when editing existing tasks
            if not self.current_user.is_superuser:
                disabled_fields = [
                    'task_completion_status',
                    'task_priority',
                    'task_title',
                    'task_detail',
                    'task_sender',
                    'receiver'
                ]
                for field in disabled_fields:
                    self.fields[field].disabled = True
                    self.fields[field].widget.attrs.update({
                        'class': 'disabled-field',
                        'title': 'This field cannot be modified due to your permission level.'
                    })

@admin.register(ManageTask)
class TaskDetailsView(admin.ModelAdmin):
    form = ManageTaskAdminForm
    list_display = [
        "task_sender",           # Task sender
        "task_title",            # Task title
        "task_detail",           # Task details
        "task_created_at",       # Task created date
        "receiver",              # Task receiver (assigned to)
        "task_deadline",         # Task deadline
        "task_priority",         # Priority of the task
        "task_progress"          # Progress of the task
    ]

    def get_form(self, request, obj=None, **kwargs):
        # Attach the current user to the form instance
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form


# Custom admin for TeamMember model
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'is_leader', 'team', 'institution', 'institution_id', 'linkedin_url', 'github_url']
    list_filter = ['team', 'is_leader']  # Filter by team and leader status
    search_fields = ['name', 'email', 'phone_number', 'team__team_name']  # Enable search on name, email, phone number, and team name
    ordering = ['team', '-is_leader', 'name']  # Sort by team, leaders first, then alphabetically by name

# Register the TeamMember model
admin.site.register(TeamMember, TeamMemberAdmin)


# Register the InternshipApplication model
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'role', 'branch', 'custom_resume')
    
    # Add filters for role and branch
    list_filter = ('role', 'branch')
    
    # Optionally, set default ordering (for example, by role or branch)
    ordering = ('role', 'branch')  # This will order the applications by role first, then branch

admin.site.register(InternshipApplication, InternshipApplicationAdmin)

