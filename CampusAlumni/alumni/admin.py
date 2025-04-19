from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, College, ProfessionalExperience, Certification, Post, CollegeNetworkRequest,UserConnection

admin.site.register(UserConnection)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_mentor', 'graduation_year')
    list_filter = ('is_staff', 'is_mentor', 'graduation_year', 'college')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_picture')}),
        (_('Education'), {'fields': ('college', 'graduation_year', 'degree')}),
        (_('Professional'), {'fields': ('current_job', 'industry', 'location', 'skills', 'linkedin_url')}),
        (_('Mentorship'), {'fields': ('is_mentor', 'mentor_bio', 'areas_of_expertise')}),
        (_('Contact'), {'fields': ('contact_email', 'contact_phone', 'college_network_opt_in')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    """Admin configuration for College model."""
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(ProfessionalExperience)
class ProfessionalExperienceAdmin(admin.ModelAdmin):
    """Admin configuration for ProfessionalExperience model."""
    list_display = ('user', 'job_title', 'company_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('user__email', 'job_title', 'company_name')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """Admin configuration for Certification model."""
    list_display = ('user', 'title', 'date')
    list_filter = ('date',)
    search_fields = ('user__email', 'title')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""
    list_display = ('user', 'created_at', 'content_preview')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'content', 'hashtags')
    
    def content_preview(self, obj):
        """Show a preview of the post content."""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    
    content_preview.short_description = 'Content'

@admin.register(CollegeNetworkRequest)
class CollegeNetworkRequestAdmin(admin.ModelAdmin):
    """Admin configuration for CollegeNetworkRequest model."""
    list_display = ('user', 'college', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at', 'college')
    search_fields = ('user__email', 'college__name')