from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class College(models.Model):
    """Information about colleges/universities."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """Custom user manager for our User model."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom user model storing alumni information."""
    username = None  # Remove username field as we'll use email instead
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_mentor = models.BooleanField(default=False)
    mentor_bio = models.TextField(blank=True, null=True)
    areas_of_expertise = models.TextField(blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    # college = models.CharField(max_length=255, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    current_job = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    short_bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)  # We'll store this as comma-separated values
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    college_network_opt_in = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_skills_list(self):
        """Return skills as a list."""
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(',')]
    
    def get_areas_of_expertise_list(self):
        """Return areas of expertise as a list."""
        if not self.areas_of_expertise:
            return []
        return [area.strip() for area in self.areas_of_expertise.split(',')]
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class ProfessionalExperience(models.Model):
    """Stores multiple work experiences per user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    class Meta:
        ordering = ['-start_date']

class Certification(models.Model):
    """Stores certifications or achievements of the user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']

class Post(models.Model):
    """Community feed where users can post content."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.TextField(blank=True)  # Store as comma-separated values
    
    def __str__(self):
        return f"Post by {self.user.get_full_name()} on {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_hashtags_list(self):
        """Return hashtags as a list."""
        if not self.hashtags:
            return []
        return [tag.strip() for tag in self.hashtags.split(',')]
    
    class Meta:
        ordering = ['-created_at']

class CollegeNetworkRequest(models.Model):
    """Stores verification requests for alumni to join a college network."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='network_requests')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='network_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request by {self.user.get_full_name()} for {self.college.name} ({self.status})"
    
    class Meta:
        ordering = ['-submitted_at']

class UserConnection(models.Model):
    """Model to represent connections between users."""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_received')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.get_full_name()} -> {self.to_user.get_full_name()} ({self.status})"
