from django.contrib import admin
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
    
    def get_recipient_names(self, obj):
        return obj.get_recipient_names()
    get_recipient_names.short_description = 'Recipients'

admin.site.register(subscribers)
admin.site.register(newsArticle)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["title","content"]
admin.site.register(Notification, NotificationAdmin)

@admin.register(developer_profile)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id","developer","job_role","points","rank"]

admin.site.register(AddTaskDetail)
class TaskDetailsView(admin.ModelAdmin):
    list_display = ["id","title","detail","created_at"]


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

